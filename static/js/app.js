// SocialMarket Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Fix account details collapsing
    const accountDetailsCollapse = document.getElementById('accountDetails');
    if (accountDetailsCollapse) {
        // Prevent auto-collapse
        accountDetailsCollapse.addEventListener('show.bs.collapse', function (e) {
            // Keep it open
        });
    }

    // Show success messages for form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Auto-hide flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('input[type="submit"], button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner me-2"></span>Processing...';

                // Re-enable after 5 seconds to prevent infinite disable
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Submit';
                }, 5000);
            }
        });
    });

    // Image preview for file uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    let preview = document.getElementById(input.id + '_preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = input.id + '_preview';
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Search functionality
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        const searchInputs = searchForm.querySelectorAll('input, select');
        searchInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Auto-submit search form when filters change
                clearTimeout(window.searchTimeout);
                window.searchTimeout = setTimeout(() => {
                    searchForm.submit();
                }, 500);
            });
        });
    }

    // Notification system
    function markNotificationRead(notificationId) {
        fetch(`/api/notifications/mark-read/${notificationId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const notification = document.getElementById(`notification-${notificationId}`);
                if (notification) {
                    notification.classList.add('opacity-50');
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Expose to global scope
    window.markNotificationRead = markNotificationRead;

    // Price formatter
    function formatPrice(amount) {
        return new Intl.NumberFormat('en-NG', {
            style: 'currency',
            currency: 'NGN',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    // Number formatter
    function formatNumber(num) {
        return new Intl.NumberFormat('en-NG').format(num);
    }

    // Copy to clipboard functionality
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        }, function(err) {
            console.error('Could not copy text: ', err);
            showToast('Failed to copy', 'error');
        });
    }

    // Toast notifications
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer') || createToastContainer();

        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        toastContainer.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = 'position: fixed; top: 0; right: 0; z-index: 9999;';
        document.body.appendChild(container);
        return container;
    }

    // Expose utility functions
    window.formatPrice = formatPrice;
    window.formatNumber = formatNumber;
    window.copyToClipboard = copyToClipboard;
    window.showToast = showToast;

    // PWA Install functionality
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;

        // Show install button
        const installButton = document.getElementById('pwa-install-btn');
        if (installButton) {
            installButton.style.display = 'block';
            installButton.addEventListener('click', async () => {
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`User response to the install prompt: ${outcome}`);
                    deferredPrompt = null;
                    installButton.style.display = 'none';
                }
            });
        }
    });

    // Handle successful app install
    window.addEventListener('appinstalled', (evt) => {
        console.log('App installed successfully');
        showToast('App installed successfully!', 'success');
    });
});

// Platform icon mapping
const platformIcons = {
    'instagram': 'fab fa-instagram',
    'facebook': 'fab fa-facebook',
    'twitter': 'fab fa-twitter',
    'tiktok': 'fab fa-tiktok',
    'youtube': 'fab fa-youtube',
    'linkedin': 'fab fa-linkedin',
    'snapchat': 'fab fa-snapchat',
    'pinterest': 'fab fa-pinterest',
    'discord': 'fab fa-discord',
    'telegram': 'fab fa-telegram',
    'whatsapp_business': 'fab fa-whatsapp'
};

// Get platform icon
function getPlatformIcon(platform) {
    return platformIcons[platform] || 'fas fa-share-alt';
}

// Format follower count
function formatFollowers(count) {
    if (count >= 1000000) {
        return (count / 1000000).toFixed(1) + 'M';
    } else if (count >= 1000) {
        return (count / 1000).toFixed(1) + 'K';
    }
    return count.toString();
}

// Validate form before submission
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Dynamic content loading
function loadContent(url, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '<div class="text-center p-4"><div class="spinner mx-auto"></div></div>';

    fetch(url)
        .then(response => response.text())
        .then(html => {
            container.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading content:', error);
            container.innerHTML = '<div class="alert alert-danger">Failed to load content</div>';
        });
}

// Expose global functions
window.getPlatformIcon = getPlatformIcon;
window.formatFollowers = formatFollowers;
window.validateForm = validateForm;
window.loadContent = loadContent;