"""
Simple Authentication Module for Streamlit App
Provides password protection for the Qase Reporter application
"""

import streamlit as st
import hashlib
from typing import Optional, Dict


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def check_simple_password() -> bool:
    """
    Simple password authentication (single password for all users)
    
    Returns:
        True if user is authenticated, False otherwise
    
    Usage in app.py:
        from auth import check_simple_password
        
        if check_simple_password():
            # Show main app
            main_app()
    """
    
    def password_entered():
        """Callback for password input"""
        # Get password from secrets
        try:
            if hasattr(st, 'secrets') and "APP_PASSWORD" in st.secrets:
                correct_password = st.secrets["APP_PASSWORD"]
            else:
                # Fallback for local development
                correct_password = "admin123"  # Change this!
                st.warning("⚠️ Using default password! Set APP_PASSWORD in secrets.toml")
            
            if st.session_state["password"] == correct_password:
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store password
            else:
                st.session_state["password_correct"] = False
                
        except Exception as e:
            st.error(f"Authentication error: {e}")
            st.session_state["password_correct"] = False

    # Check if already authenticated
    if "password_correct" not in st.session_state:
        # First run - show password input
        st.markdown("## 🔐 Authentication Required")
        st.markdown("Please enter the password to access the Qase Reporter")
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="Enter password..."
        )
        st.info("💡 Contact your admin if you don't have the password")
        return False
        
    elif not st.session_state["password_correct"]:
        # Wrong password - show error and input again
        st.markdown("## 🔐 Authentication Required")
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="Enter password..."
        )
        st.error("😕 Incorrect password. Please try again.")
        return False
        
    else:
        # Password correct
        return True


def check_multi_user_password() -> bool:
    """
    Multi-user authentication (different passwords per user)
    
    Returns:
        True if user is authenticated, False otherwise
        
    Requires in secrets.toml:
        [users]
        admin = "admin_password"
        user1 = "user1_password"
        user2 = "user2_password"
    
    Usage in app.py:
        from auth import check_multi_user_password
        
        if check_multi_user_password():
            # Show main app with st.session_state.username available
            main_app()
    """
    
    def login_entered():
        """Callback for login"""
        try:
            # Get users from secrets
            if hasattr(st, 'secrets') and "users" in st.secrets:
                users = dict(st.secrets["users"])
            else:
                # Fallback for local development
                users = {
                    "admin": "admin123",
                    "user": "user123"
                }
                st.warning("⚠️ Using default users! Configure [users] in secrets.toml")
            
            username = st.session_state["username"]
            password = st.session_state["password"]
            
            if username in users and users[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["current_user"] = username
                # Clear password from session
                del st.session_state["password"]
            else:
                st.session_state["authenticated"] = False
                
        except Exception as e:
            st.error(f"Authentication error: {e}")
            st.session_state["authenticated"] = False

    # Check if already authenticated
    if "authenticated" not in st.session_state:
        # First run - show login form
        st.markdown("## 🔐 Authentication Required")
        st.markdown("Please log in to access the Qase Reporter")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.text_input(
                "Username", 
                key="username",
                placeholder="Enter username..."
            )
            st.text_input(
                "Password", 
                type="password", 
                key="password",
                placeholder="Enter password..."
            )
            if st.button("🔓 Login", type="primary"):
                login_entered()
                st.rerun()
        
        with col2:
            st.info("""
            **Login Information:**
            - Enter your username and password
            - Contact your admin if you need access
            - Credentials are stored securely
            """)
        return False
        
    elif not st.session_state["authenticated"]:
        # Wrong credentials - show error and form again
        st.markdown("## 🔐 Authentication Required")
        st.error("😕 Invalid username or password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.text_input(
                "Username", 
                key="username",
                placeholder="Enter username..."
            )
            st.text_input(
                "Password", 
                type="password", 
                key="password",
                placeholder="Enter password..."
            )
            if st.button("🔓 Login", type="primary"):
                login_entered()
                st.rerun()
        
        with col2:
            st.warning("Please check your credentials and try again")
        return False
        
    else:
        # Authenticated - show logout button in sidebar
        with st.sidebar:
            st.success(f"✅ Logged in as: **{st.session_state.current_user}**")
            if st.button("🔒 Logout"):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.rerun()
        return True


def add_auth_to_app():
    """
    Example of how to add authentication to app.py
    
    Add this at the top of your main() function in app.py:
    
    ```python
    from auth import check_simple_password
    # OR
    from auth import check_multi_user_password
    
    def main():
        init_session_state()
        
        # Add authentication check
        if not check_simple_password():
            return  # Stop here if not authenticated
        
        # Rest of your app code...
        st.title("📊 Qase Test Run Reporter")
        # ... your existing code ...
    ```
    """
    pass


# Example usage documentation
if __name__ == "__main__":
    st.set_page_config(page_title="Auth Demo", page_icon="🔐")
    
    st.title("Authentication Demo")
    
    tab1, tab2 = st.tabs(["Simple Password", "Multi-User"])
    
    with tab1:
        st.header("Simple Password Authentication")
        if check_simple_password():
            st.success("✅ You are authenticated!")
            st.balloons()
            st.markdown("### Welcome to the protected app")
            st.info("You now have access to all features")
            
            if st.button("🔒 Logout"):
                st.session_state.password_correct = False
                st.rerun()
    
    with tab2:
        st.header("Multi-User Authentication")
        if check_multi_user_password():
            st.success(f"✅ Welcome, {st.session_state.current_user}!")
            st.balloons()
            st.markdown("### You are logged in")
            st.info(f"Current user: **{st.session_state.current_user}**")
