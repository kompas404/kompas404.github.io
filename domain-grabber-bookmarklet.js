// DOMAIN GRABBER for KOMPAS404
// Extracts domains from any target URL by regex pattern
// Usage: Load this in browser console or as bookmarklet on qanator.com / expireddomains page

(function() {
    const domains = new Set();
    const html = document.documentElement.outerHTML;
    
    // Pattern 1: Standard domain links in tables
    const pattern1 = /(?:href="https?:\/\/)?([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})(?:"|\/|\s)/g;
    let match;
    while ((match = pattern1.exec(html)) !== null) {
        const d = match[1].toLowerCase();
        // Filter out common non-domain matches
        if (!d.includes('w3.org') && !d.includes('google.com') && !d.includes('facebook.com')
            && !d.includes('twitter.com') && !d.includes('youtube.com') && !d.includes('github.com')
            && !d.includes('wikipedia.org') && !d.includes('schema.org') && d.length < 60) {
            domains.add(d);
        }
    }
    
    // Pattern 2: Namelink class (expireddomains.net)
    const pattern2 = /class="namelinks?"[^>]*>([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})</gi;
    while ((match = pattern2.exec(html)) !== null) {
        domains.add(match[1].toLowerCase());
    }
    
    // Pattern 3: qanator parked domains  
    const pattern3 = /<a[^>]*href="[^"]*([a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,})\/?"[^>]*>/gi;
    while ((match = pattern3.exec(html)) !== null) {
        const d = match[1].toLowerCase();
        if (d.length < 50) domains.add(d);
    }
    
    // Output
    const arr = [...domains].sort();
    console.log(`FOUND ${arr.length} DOMAINS:`);
    console.log(arr.join('\n'));
    
    // Copy to clipboard
    const text = arr.join('\n');
    navigator.clipboard.writeText(text).then(() => {
        alert(`Copied ${arr.length} domains to clipboard!`);
    });
    
    return arr;
})();