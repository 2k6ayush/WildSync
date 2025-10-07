# WildSync Frontend

A modern, responsive web interface for the WildSync AI-Powered Forest Management System.

## Overview

WildSync is an intelligent platform that helps forest departments analyze ecosystem data and make data-driven conservation decisions. The frontend provides an intuitive interface for uploading forest data, analyzing patterns, visualizing results, and connecting with the forest management community.

## Features

### 🌟 Core Features

- **AI-Powered Data Analysis**: Upload forest data and get intelligent insights
- **Interactive Heat Maps**: Visualize ecosystem health and risk zones
- **Expert Chatbot**: Get forest management advice from AI assistant
- **Community Hub**: Connect with forest professionals worldwide
- **Drag & Drop File Upload**: Support for CSV, Excel, PDF, and images
- **Real-time Visualizations**: Charts and graphs powered by Chart.js
- **Mobile Responsive**: Works seamlessly on all devices

### 📱 Pages & Functionality

1. **Landing Page** (`index.html`)
   - Hero section with feature highlights
   - How it works section
   - Call-to-action areas
   - Professional forest-themed design

2. **Authentication** (`login.html`, `register.html`)
   - User registration and login
   - Form validation and error handling
   - Secure password requirements
   - Remember me functionality

3. **Dashboard** (`dashboard.html`)
   - Overview with key metrics
   - File upload with drag & drop
   - Data analysis and visualization
   - Interactive heat maps with Leaflet
   - AI chatbot integration
   - Report generation tools

4. **Community** (`community.html`)
   - Forum discussions by category
   - Case studies from around the world
   - Resource library
   - Knowledge sharing platform

## Technology Stack

### Frontend Technologies
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with CSS Custom Properties
- **JavaScript ES6+**: Modern JavaScript with async/await
- **Chart.js**: Data visualization and charts
- **Leaflet**: Interactive mapping
- **Responsive Design**: Mobile-first approach

### Design System
- **Color Palette**: Forest-themed green color scheme
- **Typography**: Clean, professional fonts
- **Components**: Reusable UI components
- **Icons**: Emoji-based icons for universal recognition

## File Structure

```
frontend/
├── index.html                 # Landing page
├── login.html                # Login page  
├── register.html             # Registration page
├── dashboard.html            # Main application dashboard
├── community.html            # Community forum and resources
├── static/
│   ├── css/
│   │   └── main.css          # Main stylesheet
│   ├── js/
│   │   └── main.js           # Core JavaScript functionality
│   └── images/               # Image assets
├── templates/                # Additional templates
└── README.md                 # This file
```

## API Integration

The frontend is designed to work seamlessly with the WildSync backend API:

### Endpoints Used
- `/api/auth/*` - Authentication (login, register, profile)
- `/api/uploads` - File upload functionality
- `/api/analysis/*` - Data analysis and insights
- `/api/maps/*` - Heat map data and layers
- `/api/chatbot` - AI assistant interactions
- `/api/community/*` - Forum posts and case studies

### Authentication
- Session-based authentication with cookies
- Automatic login state management
- Secure logout functionality
- Protected routes for authenticated users

## Key Components

### 1. Authentication System (`WildSync.Auth`)
```javascript
// Login user
await WildSync.Auth.login(email, password);

// Register new user  
await WildSync.Auth.register(name, email, password);

// Check if user is logged in
const isLoggedIn = WildSync.Auth.isLoggedIn();

// Get current user
const user = WildSync.Auth.currentUser;
```

### 2. File Upload (`WildSync.FileUpload`)
```javascript
// Initialize drag and drop
WildSync.FileUpload.initDragAndDrop(uploadArea, fileInput, handleFileUpload);

// Upload file
const result = await WildSync.FileUpload.uploadFile(file);
```

### 3. API Utilities (`WildSync.API`)
```javascript
// Generic API call
const data = await WildSync.API.call('/api/endpoint', options);

// Upload file
const result = await WildSync.API.uploads.upload(file);

// Send chat message
const response = await WildSync.API.chatbot.sendMessage(message);
```

### 4. Chat Interface (`WildSync.ChatManager`)
```javascript
// Initialize chatbot
WildSync.ChatManager.init('chat-container');

// Add message programmatically
WildSync.ChatManager.addMessage('Hello!', false);
```

### 5. Utilities (`WildSync.Utils`)
```javascript
// Show notification
WildSync.Utils.showAlert('Success!', 'success');

// Format date
const formatted = WildSync.Utils.formatDate(dateString);

// Validate email
const isValid = WildSync.Utils.isValidEmail(email);
```

## Responsive Design

The website is fully responsive and works across all device sizes:

### Desktop (1200px+)
- Full sidebar navigation
- Multi-column layouts
- Large interactive elements

### Tablet (768px - 1199px)  
- Adapted sidebar
- Flexible grid layouts
- Touch-optimized interactions

### Mobile (< 768px)
- Collapsible navigation
- Single-column layouts
- Mobile-optimized forms
- Swipe-friendly interfaces

## Browser Support

- **Modern Browsers**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **JavaScript**: ES6+ features used (async/await, arrow functions, etc.)
- **CSS**: CSS Custom Properties, Flexbox, Grid
- **Progressive Enhancement**: Core functionality works without JavaScript

## Getting Started

### Prerequisites
- A web server (Apache, Nginx, or development server)
- WildSync backend API running
- Modern web browser

### Installation

1. **Clone or download the frontend files**
   ```bash
   # Files are already in the frontend/ directory
   cd frontend/
   ```

2. **Serve the files**
   ```bash
   # Using Python's built-in server
   python -m http.server 8080
   
   # Or using Node.js
   npx serve -p 8080
   
   # Or use any web server
   ```

3. **Access the application**
   ```
   http://localhost:8080
   ```

### Configuration

Update the API base URL in `static/js/main.js` if needed:

```javascript
const API_BASE = '/api';  // Change this to your backend URL
```

## Development

### Code Organization
- **Modular JavaScript**: All functionality organized into namespaced modules
- **Consistent Naming**: Clear, descriptive variable and function names
- **Error Handling**: Comprehensive error handling throughout
- **Loading States**: User feedback during async operations

### Best Practices
- **Accessibility**: Semantic HTML, proper ARIA labels, keyboard navigation
- **Performance**: Optimized images, minified CSS/JS in production
- **SEO**: Proper meta tags, structured data, semantic markup
- **Security**: XSS prevention, CSRF protection, input validation

### Adding New Features

1. **Add HTML structure** in the appropriate page
2. **Style with CSS** using the existing design system
3. **Add JavaScript functionality** following the modular pattern
4. **Test responsiveness** across different screen sizes
5. **Test API integration** with backend endpoints

## Deployment

### Production Checklist
- [ ] Minify CSS and JavaScript files
- [ ] Optimize images (WebP format where supported)
- [ ] Configure proper HTTP headers (caching, security)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CDN for static assets
- [ ] Test all functionality in production environment

### Environment Variables
The frontend adapts based on the backend configuration. Ensure:
- API endpoints are accessible
- CORS is properly configured
- Session cookies work across domains (if needed)

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Check that backend is running
   - Verify API base URL is correct
   - Check CORS configuration

2. **Authentication Issues**  
   - Clear browser cookies/session storage
   - Check network tab for failed requests
   - Verify backend session handling

3. **File Upload Problems**
   - Check file size limits
   - Verify supported file types
   - Check backend upload configuration

4. **Map Not Loading**
   - Check internet connection (Leaflet requires CDN)
   - Verify map container has proper height/width
   - Check console for JavaScript errors

## Contributing

When contributing to the frontend:

1. **Follow existing code style** and patterns
2. **Test on multiple browsers** and devices
3. **Update documentation** for new features
4. **Use semantic commit messages**
5. **Ensure accessibility compliance**

## License

This frontend is part of the WildSync project. See main project license for details.

## Support

For support and questions:
- Check the main WildSync documentation
- Review the browser console for error messages
- Test API endpoints independently
- Verify network connectivity and CORS settings

---

**WildSync Frontend** - Built with 💚 for forest conservation