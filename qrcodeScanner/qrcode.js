let currentQR = null;

        // Generate QR Code
        function generateQR() {
            const text = document.getElementById('qrText').value.trim();
            const size = parseInt(document.getElementById('qrSize').value);
            const foreground = document.getElementById('foregroundColor').value;
            const background = document.getElementById('backgroundColor').value;
            const level = document.getElementById('errorLevel').value;
            
            if (!text) {
                alert('Please enter some content for your QR code');
                return;
            }
            
            // Hide placeholder and show canvas
            document.getElementById('qrPlaceholder').style.display = 'none';
            const canvas = document.getElementById('qrcode');
            canvas.style.display = 'block';
            
            // Generate QR code
            currentQR = new QRious({
                element: canvas,
                value: text,
                size: size,
                background: background,
                foreground: foreground,
                level: level
            });
            
            // Show QR info
            document.getElementById('qrInfo').style.display = 'block';
            document.getElementById('qrContent').textContent = text;
        }

        // Download QR Code
        function downloadQR(format) {
            if (!currentQR) {
                alert('Please generate a QR code first');
                return;
            }
            
            const canvas = document.getElementById('qrcode');
            const text = document.getElementById('qrText').value;
            const filename = `qrcode_${Date.now()}`;
            
            if (format === 'png') {
                const link = document.createElement('a');
                link.download = filename + '.png';
                link.href = canvas.toDataURL('image/png');
                link.click();
            } else if (format === 'svg') {
                // Create SVG version
                const size = currentQR.size;
                const foreground = document.getElementById('foregroundColor').value;
                const background = document.getElementById('backgroundColor').value;
                const level = document.getElementById('errorLevel').value;
                
                const svgQR = new QRious({
                    value: text,
                    size: size,
                    background: background,
                    foreground: foreground,
                    level: level
                });
                
                // Convert to SVG
                const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svgElement.setAttribute('width', size);
                svgElement.setAttribute('height', size);
                svgElement.setAttribute('viewBox', `0 0 ${size} ${size}`);
                
                // Create image element in SVG
                const image = document.createElementNS('http://www.w3.org/2000/svg', 'image');
                image.setAttribute('width', size);
                image.setAttribute('height', size);
                image.setAttribute('href', canvas.toDataURL('image/png'));
                
                svgElement.appendChild(image);
                
                const svgData = new XMLSerializer().serializeToString(svgElement);
                const svgBlob = new Blob([svgData], { type: 'image/svg+xml' });
                const svgUrl = URL.createObjectURL(svgBlob);
                
                const link = document.createElement('a');
                link.download = filename + '.svg';
                link.href = svgUrl;
                link.click();
                
                URL.revokeObjectURL(svgUrl);
            }
        }

        // Generate initial QR code on page load
        window.addEventListener('load', function() {
            generateQR();
        });

        // Auto-generate when content changes
        document.getElementById('qrText').addEventListener('input', function() {
            if (this.value.trim()) {
                generateQR();
            }
        });

        // Auto-generate when settings change
        ['qrSize', 'foregroundColor', 'backgroundColor', 'errorLevel'].forEach(id => {
            document.getElementById(id).addEventListener('change', function() {
                if (document.getElementById('qrText').value.trim()) {
                    generateQR();
                }
            });
        });