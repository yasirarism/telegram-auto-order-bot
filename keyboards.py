from pyrogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from typing import List

def get_main_keyboard():
    """Get main keyboard with all menu options"""
    keyboard = [
        [KeyboardButton("🏠 Start"), KeyboardButton("💬 Private Message")],
        [KeyboardButton("📦 Katalog"), KeyboardButton("📊 Stok")],
        [KeyboardButton("👤 Informasi Akun"), KeyboardButton("💰 Deposit")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_product_number_keyboard(products: List, current_page: int = 0, total_pages: int = 1):
    """Get keyboard with product numbers and navigation"""
    keyboard = []
    
    # Add product number buttons (1-10)
    row = []
    for i, product in enumerate(products, 1):
        row.append(KeyboardButton(str(i)))
        if i % 5 == 0:  # 5 buttons per row
            keyboard.append(row)
            row = []
    
    if row:  # Add remaining buttons
        keyboard.append(row)
    
    # Add navigation buttons if needed
    if total_pages > 1:
        nav_row = []
        if current_page > 0:
            nav_row.append(KeyboardButton("⬅️ Sebelumnya"))
        if current_page < total_pages - 1:
            nav_row.append(KeyboardButton("➡️ Selanjutnya"))
        if nav_row:
            keyboard.append(nav_row)
    
    # Add back button
    keyboard.append([KeyboardButton("🔙 Kembali")])
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_start_inline_keyboard():
    """Get inline keyboard for start command"""
    keyboard = [
        [
            InlineKeyboardButton("🏆 Produk Teratas", callback_data="top_products"),
            InlineKeyboardButton("👥 Pembeli Teratas", callback_data="top_buyers")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_checkout_keyboard(product_id: str):
    """Get inline keyboard for product checkout"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Beli Sekarang", callback_data=f"buy_{product_id}"),
            InlineKeyboardButton("❌ Batal", callback_data="cancel_checkout")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_deposit_keyboard(user_id: int):
    """Get inline keyboard for admin deposit options"""
    keyboard = [
        [
            InlineKeyboardButton("💵 +10,000", callback_data=f"deposit_{user_id}_10000"),
            InlineKeyboardButton("💵 +25,000", callback_data=f"deposit_{user_id}_25000"),
        ],
        [
            InlineKeyboardButton("💵 +50,000", callback_data=f"deposit_{user_id}_50000"),
            InlineKeyboardButton("💵 +100,000", callback_data=f"deposit_{user_id}_100000"),
        ],
        [
            InlineKeyboardButton("✏️ Custom Amount", callback_data=f"deposit_{user_id}_custom"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pagination_keyboard(current_page: int, total_pages: int, prefix: str = "page"):
    """Get inline keyboard for pagination"""
    keyboard = []
    nav_row = []
    
    if current_page > 0:
        nav_row.append(InlineKeyboardButton("⬅️", callback_data=f"{prefix}_{current_page-1}"))
    
    nav_row.append(InlineKeyboardButton(f"{current_page+1}/{total_pages}", callback_data="page_info"))
    
    if current_page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("➡️", callback_data=f"{prefix}_{current_page+1}"))
    
    keyboard.append(nav_row)
    return InlineKeyboardMarkup(keyboard)
