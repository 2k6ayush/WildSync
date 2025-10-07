// WildSync - Main JavaScript File
// API utilities, authentication, and common functionality

// Configuration
const API_BASE = '/api';
const CONFIG = {
    endpoints: {
        auth: `${API_BASE}/auth`,
        uploads: `${API_BASE}/uploads`,
        analysis: `${API_BASE}/analysis`,
        maps: `${API_BASE}/maps`,
        chatbot: `${API_BASE}/chatbot`,
        community: `${API_BASE}/community`,
        profile: `${API_BASE}/profile`
    }
};

// Utility Functions
const Utils = {
    // Show loading spinner
    showLoading(element) {
        if (element) {
            element.innerHTML = '<div class="spinner"></div>';
        }
    },

    // Hide loading spinner
    hideLoading(element, content = '') {
        if (element) {
            element.innerHTML = content;
        }
    },

    // Show alert message
    showAlert(message, type = 'success', container = null) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        const targetContainer = container || document.querySelector('.main-content') || document.body;
        targetContainer.insertBefore(alertDiv, targetContainer.firstChild);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    },

    // Format date
    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Validate email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Generate UUID for temporary IDs
    generateId() {
        return 'id-' + Math.random().toString(36).substr(2, 16);
    }
};

// API Helper
const API = {
    // Generic API call
    async call(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include', // For session management
        };

        const finalOptions = { ...defaultOptions, ...options };
        
        if (finalOptions.body && typeof finalOptions.body === 'object') {
            finalOptions.body = JSON.stringify(finalOptions.body);
        }

        try {
            const response = await fetch(endpoint, finalOptions);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP error! status: ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Authentication methods
    auth: {
        async login(email, password) {
            return API.call(`${CONFIG.endpoints.auth}/login`, {
                method: 'POST',
                body: { email, password }
            });
        },

        async register(name, email, password) {
            return API.call(`${CONFIG.endpoints.auth}/register`, {
                method: 'POST',
                body: { name, email, password }
            });
        },

        async logout() {
            return API.call(`${CONFIG.endpoints.auth}/logout`, {
                method: 'POST'
            });
        },

        async getProfile() {
            return API.call(`${CONFIG.endpoints.auth}/me`);
        }
    },

    // File upload methods
    uploads: {
        async upload(file, progressCallback = null) {
            const formData = new FormData();
            formData.append('file', file);

            const options = {
                method: 'POST',
                body: formData,
                credentials: 'include'
            };

            // Remove Content-Type header for FormData
            delete options.headers;

            return API.call(CONFIG.endpoints.uploads, options);
        }
    },

    // Analysis methods
    analysis: {
        async start(forestId) {
            return API.call(`${CONFIG.endpoints.analysis}/start`, {
                method: 'POST',
                body: { forest_id: forestId }
            });
        }
    },

    // Maps methods
    maps: {
        async getLayers(analysisId) {
            return API.call(`${CONFIG.endpoints.maps}/layers?analysis_id=${analysisId}`);
        }
    },

    // Chatbot methods
    chatbot: {
        async sendMessage(message, forestId = null) {
            return API.call(CONFIG.endpoints.chatbot, {
                method: 'POST',
                body: { message, forest_id: forestId }
            });
        }
    },

    // Community methods
    community: {
        async getCaseStudies(location = null) {
            let url = `${CONFIG.endpoints.community}/case-studies`;
            if (location) {
                url += `?location=${encodeURIComponent(location)}`;
            }
            return API.call(url);
        },

        async getForumPosts(category = null) {
            let url = `${CONFIG.endpoints.community}/forum`;
            if (category) {
                url += `?category=${encodeURIComponent(category)}`;
            }
            return API.call(url);
        },

        async createPost(title, content, category = null) {
            return API.call(`${CONFIG.endpoints.community}/forum`, {
                method: 'POST',
                body: { title, content, category }
            });
        }
    }
};

// Authentication Manager
const Auth = {
    currentUser: null,

    // Check if user is logged in
    isLoggedIn() {
        return this.currentUser !== null;
    },

    // Initialize auth state
    async init() {
        try {
            const profile = await API.auth.getProfile();
            this.currentUser = profile.user;
            this.updateUI();
            return true;
        } catch (error) {
            this.currentUser = null;
            this.updateUI();
            return false;
        }
    },

    // Login user
    async login(email, password) {
        try {
            const result = await API.auth.login(email, password);
            this.currentUser = result.user;
            this.updateUI();
            Utils.showAlert('Successfully logged in!', 'success');
            return true;
        } catch (error) {
            Utils.showAlert(error.message, 'error');
            return false;
        }
    },

    // Register user
    async register(name, email, password) {
        try {
            await API.auth.register(name, email, password);
            Utils.showAlert('Registration successful! Please log in.', 'success');
            return true;
        } catch (error) {
            Utils.showAlert(error.message, 'error');
            return false;
        }
    },

    // Logout user
    async logout() {
        try {
            await API.auth.logout();
            this.currentUser = null;
            this.updateUI();
            Utils.showAlert('Successfully logged out!', 'success');
            window.location.href = 'index.html';
        } catch (error) {
            Utils.showAlert(error.message, 'error');
        }
    },

    // Update UI based on auth state
    updateUI() {
        const loginBtn = document.getElementById('login-btn');
        const registerBtn = document.getElementById('register-btn');
        const logoutBtn = document.getElementById('logout-btn');
        const dashboardBtn = document.getElementById('dashboard-btn');
        const userProfile = document.getElementById('user-profile');

        if (this.isLoggedIn()) {
            // User is logged in
            if (loginBtn) loginBtn.style.display = 'none';
            if (registerBtn) registerBtn.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'inline-block';
            if (dashboardBtn) dashboardBtn.style.display = 'inline-block';
            if (userProfile) {
                userProfile.style.display = 'block';
                userProfile.textContent = `Welcome, ${this.currentUser.name}`;
            }
        } else {
            // User is not logged in
            if (loginBtn) loginBtn.style.display = 'inline-block';
            if (registerBtn) registerBtn.style.display = 'inline-block';
            if (logoutBtn) logoutBtn.style.display = 'none';
            if (dashboardBtn) dashboardBtn.style.display = 'none';
            if (userProfile) userProfile.style.display = 'none';
        }
    },

    // Require authentication for certain pages
    requireAuth() {
        if (!this.isLoggedIn()) {
            Utils.showAlert('Please log in to access this page.', 'warning');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
            return false;
        }
        return true;
    }
};

// File Upload Manager
const FileUpload = {
    // Initialize drag and drop
    initDragAndDrop(uploadArea, fileInput, onUpload) {
        if (!uploadArea) return;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
        });

        // Handle dropped files
        uploadArea.addEventListener('drop', handleDrop, false);
        uploadArea.addEventListener('click', () => fileInput.click());

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFiles(files);
        }

        function handleFiles(files) {
            ([...files]).forEach(onUpload);
        }

        // Also handle file input change
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });
    },

    // Upload single file
    async uploadFile(file, progressCallback = null) {
        try {
            if (progressCallback) progressCallback(0);
            
            const result = await API.uploads.upload(file, progressCallback);
            
            if (progressCallback) progressCallback(100);
            
            Utils.showAlert(`File "${file.name}" uploaded successfully!`, 'success');
            return result;
        } catch (error) {
            Utils.showAlert(`Failed to upload "${file.name}": ${error.message}`, 'error');
            throw error;
        }
    }
};

// Chat Manager
const ChatManager = {
    chatContainer: null,
    messagesContainer: null,
    inputField: null,
    sendButton: null,

    // Initialize chat interface
    init(containerId) {
        this.chatContainer = document.getElementById(containerId);
        if (!this.chatContainer) return;

        this.messagesContainer = this.chatContainer.querySelector('.chat-messages');
        this.inputField = this.chatContainer.querySelector('.chat-input');
        this.sendButton = this.chatContainer.querySelector('.chat-send-btn');

        if (this.sendButton) {
            this.sendButton.addEventListener('click', () => this.sendMessage());
        }

        if (this.inputField) {
            this.inputField.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }
    },

    // Add message to chat
    addMessage(message, isUser = false) {
        if (!this.messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;
        messageDiv.textContent = message;

        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    },

    // Send message
    async sendMessage() {
        if (!this.inputField || !this.inputField.value.trim()) return;

        const message = this.inputField.value.trim();
        this.inputField.value = '';

        // Add user message
        this.addMessage(message, true);

        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chat-message bot typing';
        typingDiv.textContent = 'AI is thinking...';
        this.messagesContainer.appendChild(typingDiv);

        try {
            const result = await API.chatbot.sendMessage(message);
            
            // Remove typing indicator
            typingDiv.remove();
            
            // Add bot response
            this.addMessage(result.response);
        } catch (error) {
            // Remove typing indicator
            typingDiv.remove();
            
            this.addMessage('Sorry, I encountered an error. Please try again.');
            Utils.showAlert(`Chat error: ${error.message}`, 'error');
        }
    }
};

// Navigation Manager
const Navigation = {
    // Initialize navigation
    init() {
        // Add active class to current page
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('.nav-menu a, .sidebar-menu a');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPage || (currentPage === '' && href === 'index.html')) {
                link.classList.add('active');
            }
        });

        // Handle mobile menu toggle (if needed)
        const menuToggle = document.querySelector('.menu-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (menuToggle && navMenu) {
            menuToggle.addEventListener('click', () => {
                navMenu.classList.toggle('show');
            });
        }
    }
};

// Form Validation
const FormValidator = {
    // Validate form field
    validateField(field, rules) {
        const value = field.value.trim();
        const errors = [];

        // Required validation
        if (rules.required && !value) {
            errors.push(`${field.name || 'This field'} is required`);
        }

        // Email validation
        if (rules.email && value && !Utils.isValidEmail(value)) {
            errors.push('Please enter a valid email address');
        }

        // Min length validation
        if (rules.minLength && value.length < rules.minLength) {
            errors.push(`Must be at least ${rules.minLength} characters long`);
        }

        // Password confirmation
        if (rules.confirmPassword && value !== rules.confirmPassword) {
            errors.push('Passwords do not match');
        }

        // Update UI
        this.updateFieldUI(field, errors);
        
        return errors.length === 0;
    },

    // Update field UI based on validation
    updateFieldUI(field, errors) {
        const errorContainer = field.parentNode.querySelector('.form-error');
        
        if (errors.length > 0) {
            field.classList.add('error');
            if (errorContainer) {
                errorContainer.textContent = errors[0];
            }
        } else {
            field.classList.remove('error');
            if (errorContainer) {
                errorContainer.textContent = '';
            }
        }
    },

    // Validate entire form
    validateForm(form, validationRules) {
        let isValid = true;
        
        for (const fieldName in validationRules) {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                const fieldValid = this.validateField(field, validationRules[fieldName]);
                if (!fieldValid) isValid = false;
            }
        }
        
        return isValid;
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize authentication
    await Auth.init();
    
    // Initialize navigation
    Navigation.init();
    
    // Add global error handler
    window.addEventListener('error', (e) => {
        console.error('Global error:', e.error);
        Utils.showAlert('An unexpected error occurred. Please refresh the page.', 'error');
    });
    
    // Add unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (e) => {
        console.error('Unhandled promise rejection:', e.reason);
        Utils.showAlert('An unexpected error occurred. Please try again.', 'error');
    });
});

// Export for use in other files
window.WildSync = {
    Utils,
    API,
    Auth,
    FileUpload,
    ChatManager,
    Navigation,
    FormValidator,
    CONFIG
};