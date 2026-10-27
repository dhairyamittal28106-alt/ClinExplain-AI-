"""
Text Highlighter Utility

Highlights source quotes in original report text.
"""

from typing import List, Set


def highlight_source_quotes(text: str, source_quotes: List[str]) -> str:
    """
    Highlight source quotes in text with HTML spans.
    
    Args:
        text: Original text
        source_quotes: List of quotes to highlight
        
    Returns:
        HTML with highlighted quotes
    """
    highlighted = text
    
    
    sorted_quotes = sorted(set(source_quotes), key=len, reverse=True)
    
    for quote in sorted_quotes:
        if quote and quote in highlighted:
            highlighted = highlighted.replace(
                quote,
                f'<span class="source-highlight">{quote}</span>'
            )
    
    return highlighted


def extract_source_quotes_from_extraction(extraction: dict) -> Set[str]:
    """
    Extract all source quotes from extraction result.
    
    Args:
        extraction: Extraction dictionary
        
    Returns:
        Set of source quotes
    """
    quotes = set()
    
    
    for finding in extraction.get('findings', []):
        if 'source_quote' in finding and finding['source_quote']:
            quotes.add(finding['source_quote'])
    
    
    for flag in extraction.get('attention_flags', []):
        if 'source_quote' in flag and flag['source_quote']:
            quotes.add(flag['source_quote'])
    
    
    for term in extraction.get('terminology', []):
        if 'source_quote' in term and term['source_quote']:
            quotes.add(term['source_quote'])
    
    return quotes
