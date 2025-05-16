"""
Helper utility functions for the AgentVerse platform.
"""
import hashlib
from datetime import datetime
import streamlit as st

def format_date(date):
    """Format a date for display"""
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return date.strftime("%Y-%m-%d %H:%M")

def format_number(number):
    """Format a number for display"""
    if isinstance(number, str):
        try:
            number = float(number)
        except ValueError:
            return number
            
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    return str(number)

def format_ftn(amount):
    """Format FTN amount for display"""
    try:
        if isinstance(amount, str):
            # If it's a string like "100 FTN", extract the number
            amount = float(amount.split()[0])
        return f"{amount:,.2f} FTN"
    except (ValueError, IndexError):
        return amount

def format_percentage(value):
    """Format percentage for display"""
    try:
        return f"{float(value):.1f}%"
    except ValueError:
        return value

def format_duration(seconds):
    """Format duration for display"""
    try:
        seconds = float(seconds)
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    except ValueError:
        return seconds

def format_file_size(bytes_value):
    """Format file size for display"""
    try:
        bytes_value = float(bytes_value)
        if bytes_value < 1024:
            return f"{bytes_value}B"
        elif bytes_value < 1024 * 1024:
            return f"{bytes_value/1024:.1f}KB"
        elif bytes_value < 1024 * 1024 * 1024:
            return f"{bytes_value/(1024*1024):.1f}MB"
        else:
            return f"{bytes_value/(1024*1024*1024):.1f}GB"
    except ValueError:
        return bytes_value

def format_cid(cid):
    """Format IPFS CID for display"""
    if isinstance(cid, str) and len(cid) > 10:
        return f"{cid[:6]}...{cid[-4:]}"
    return cid

def format_tx_hash(tx_hash):
    """Format transaction hash for display"""
    if isinstance(tx_hash, str) and len(tx_hash) > 10:
        return f"{tx_hash[:6]}...{tx_hash[-4:]}"
    return tx_hash

def format_address(address):
    """Format blockchain address for display"""
    if isinstance(address, str) and len(address) > 10:
        return f"{address[:6]}...{address[-4:]}"
    return address

def calculate_hash(content):
    """Calculate SHA-256 hash of content"""
    if isinstance(content, str):
        content = content.encode()
    return "0x" + hashlib.sha256(content).hexdigest()

def show_notification(message, type="info", duration=3):
    """Show a temporary notification"""
    if type == "success":
        notification = st.success(message)
    elif type == "error":
        notification = st.error(message)
    elif type == "warning":
        notification = st.warning(message)
    else:
        notification = st.info(message)
        
    # Use st.empty() to clear after duration in production code
    # Here we'll leave it visible as Streamlit can't do auto-dismiss easily 