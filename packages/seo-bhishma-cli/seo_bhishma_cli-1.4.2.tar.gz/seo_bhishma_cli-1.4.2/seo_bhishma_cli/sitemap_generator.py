import click
import pandas as pd
from lxml import etree
import gzip
import os
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
from rich import print as rprint

console = Console()

# Generate a sitemap XML string
def generate_sitemap(urls, priority=None, frequency=None, lastmod=None):
    urlset = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    comment = etree.Comment("Generated by seo-bhishma-cli tool")
    urlset.append(comment)
    for url in urls:
        url_element = etree.Element('url')
        loc_element = etree.Element('loc')
        loc_element.text = url
        url_element.append(loc_element)
        if lastmod:
            lastmod_element = etree.Element('lastmod')
            lastmod_element.text = lastmod
            url_element.append(lastmod_element)
        if priority:
            priority_element = etree.Element('priority')
            priority_element.text = priority
            url_element.append(priority_element)
        if frequency:
            frequency_element = etree.Element('changefreq')
            frequency_element.text = frequency
            url_element.append(frequency_element)
        urlset.append(url_element)
    return etree.tostring(urlset, pretty_print=True, xml_declaration=True, encoding='UTF-8')

# Write sitemap to file
def write_sitemap(file_path, sitemap_content, compressed=False):
    try:
        if compressed:
            with gzip.open(file_path, 'wb', encoding='utf-8') as f:
                f.write(sitemap_content)
        else:
            with open(file_path, 'wb', encoding='utf-8') as f:
                f.write(sitemap_content)
    except Exception as e:
        console.log(f"[bold red][-] Failed to write sitemap to file: {e}[/bold red]")

# Read input CSV file
def read_input_file(file_path):
    try:
        return pd.read_csv(file_path)['url'].tolist()
    except Exception as e:
        console.log(f"[bold red][-] Failed to read input file: {e}[/bold red]")
        return []

@click.command()
@click.pass_context
def sitemap_generator(ctx):
    """Generate XML sitemaps from a list of URLs."""
    while True:
        console.print("\n" + "="*50, style="bold magenta")
        console.print("Sitemap Generator", style="bold yellow")
        console.print("1. Generate a single sitemap", style="cyan")
        console.print("2. Generate nested sitemaps", style="cyan")
        console.print("3. Exit", style="bold red")
        choice = Prompt.ask("[cyan bold]Enter your choice[/cyan bold]", choices=["1", "2", "3"])

        if choice == "3":
            console.print("Exiting Sitemap Generator. Goodbye!", style="bold red")
            break
        elif choice in ["1", "2"]:
            input_file = Prompt.ask("[cyan]Enter the path to the input CSV file[/cyan]", default="input.csv")
            output_dir = Prompt.ask("[cyan]Enter the output directory[/cyan]", default=os.getcwd())
            
            if not os.path.exists(output_dir):
                console.print(f"[bold red][-] Output directory '{output_dir}' does not exist.[/bold red]")
                console.print("[bold red][-] Please create the directory and try again.[/bold red]")
                continue

            nested = choice == "2"
            url_limit = 50000
            if nested:
                url_limit = int(Prompt.ask("[cyan]Enter the maximum number of URLs per sitemap[/cyan]", default=50000, show_default=True))
            compressed = Prompt.ask("[cyan]Do you want to create compressed sitemaps? (yes/no)[/cyan]", default="no") == "yes"
            priority = Prompt.ask("[cyan]Enter priority for URLs (or leave blank)[/cyan]", default='', show_default=False)
            frequency = Prompt.ask("[cyan]Enter change frequency for URLs (or leave blank)[/cyan]", default='', show_default=False)
            lastmod = Prompt.ask("[cyan]Enter the last modified date for URLs (or leave blank for current time)[/cyan]", default='', show_default=False)
            if not lastmod:
                lastmod = datetime.now().strftime('%Y-%m-%d')

            urls = read_input_file(input_file)
            if not urls:
                console.print("[bold red][-] No URLs found in the input file.[/bold red]")
                continue
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            try:
                if not nested:
                    # Single sitemap
                    console.print("[+] Generating single sitemap...", style="bold green")
                    sitemap_content = generate_sitemap(urls, priority if priority else None, frequency if frequency else None, lastmod)
                    file_name = f'sitemap_{timestamp}.xml'
                    file_path = os.path.join(output_dir, file_name)
                    if compressed:
                        file_path += '.gz'
                    write_sitemap(file_path, sitemap_content, compressed)
                    console.print(f"[+] Single sitemap saved to {file_path}", style="bold green")
                else:
                    # Nested sitemaps
                    console.print("[+] Generating nested sitemaps...", style="bold green")
                    sitemap_index = []
                    with Progress() as progress:
                        task = progress.add_task("[green][+] Creating sitemaps...", total=(len(urls) // url_limit) + 1)
                        for i in range(0, len(urls), url_limit):
                            sitemap_urls = urls[i:i+url_limit]
                            sitemap_content = generate_sitemap(sitemap_urls, priority if priority else None, frequency if frequency else None, lastmod)
                            sitemap_file_name = f'sitemap_{timestamp}_{i // url_limit}.xml'
                            sitemap_file_path = os.path.join(output_dir, sitemap_file_name)
                            if compressed:
                                sitemap_file_path += '.gz'
                            write_sitemap(sitemap_file_path, sitemap_content, compressed)
                            sitemap_index.append(sitemap_file_name if not compressed else sitemap_file_name + '.gz')
                            progress.advance(task)
                    
                    # Generate sitemap index
                    sitemapindex = etree.Element('sitemapindex', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
                    comment = etree.Comment("Generated by seo-bhishma-cli tool")
                    sitemapindex.append(comment)
                    for sitemap in sitemap_index:
                        sitemap_element = etree.Element('sitemap')
                        loc_element = etree.Element('loc')
                        loc_element.text = os.path.join(output_dir, sitemap)
                        sitemap_element.append(loc_element)
                        sitemapindex.append(sitemap_element)
                    
                    sitemap_index_content = etree.tostring(sitemapindex, pretty_print=True, xml_declaration=True, encoding='UTF-8')
                    sitemap_index_file = f'sitemap_index_{timestamp}.xml'
                    sitemap_index_path = os.path.join(output_dir, sitemap_index_file)
                    if compressed:
                        sitemap_index_path += '.gz'
                    write_sitemap(sitemap_index_path, sitemap_index_content, compressed)
                    console.print(f"[+] Sitemap index saved to {sitemap_index_path}", style="bold green")
                    console.print(f"[+] Total sitemaps created: {len(sitemap_index)}", style="bold green")
            except Exception as e:
                console.log(f"[bold red][-] An error occurred while generating the sitemaps: {e}[/bold red]")
        else:
            console.print("[-] Invalid choice. Please select a valid option.", style="bold red")

        console.print("\n" + "="*50 + "\n", style="bold magenta")

if __name__ == '__main__':
    sitemap_generator()