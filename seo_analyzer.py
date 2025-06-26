import requests
from bs4 import BeautifulSoup
import trafilatura
from urllib.parse import urlparse, urljoin
import whois
from datetime import datetime
import time
import re
from typing import Dict, List, Tuple

class SEOAnalyzer:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def analyze(self):
        """Perform complete SEO analysis of the website"""
        start_time = time.time()

        # Fetch page content
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main text content
        downloaded = trafilatura.fetch_url(self.url)
        text_content = trafilatura.extract(downloaded)

        # Perform various analyses
        meta_analysis = self.analyze_meta_tags(soup)
        content_analysis = self.analyze_content(soup, text_content)
        technical_analysis = self.analyze_technical(response, soup)
        speed_analysis = self.analyze_speed(response)
        security_analysis = self.analyze_security()
        link_analysis = self.analyze_links(soup)

        # Generate improvements
        improvements = self.generate_improvements(
            meta_analysis, content_analysis, technical_analysis,
            speed_analysis, security_analysis, link_analysis
        )

        # Calculate scores
        scores = self.calculate_scores(
            meta_analysis, content_analysis, technical_analysis,
            speed_analysis, security_analysis, link_analysis
        )

        return {
            'overall_score': scores['overall'],
            'metrics': {
                'Meta Tags': scores['meta'],
                'Content': scores['content'],
                'Technical': scores['technical'],
                'Speed': scores['speed'],
                'Security': scores['security'],
                'Links': scores['links']
            },
            'load_time': time.time() - start_time,
            'mobile_friendly': self.check_mobile_friendly(),
            'ssl_certified': self.url.startswith('https'),
            'meta_analysis': meta_analysis,
            'content_analysis': content_analysis,
            'technical_analysis': technical_analysis,
            'speed_analysis': speed_analysis,
            'security_analysis': security_analysis,
            'link_analysis': link_analysis,
            'improvements': improvements
        }

    def analyze_meta_tags(self, soup) -> List[str]:
        """Enhanced meta tags analysis"""
        analysis = []

        # Title analysis
        title = soup.title.string if soup.title else None
        if title:
            title_length = len(title)
            if title_length < 30:
                analysis.append(f"Title tag is too short ({title_length} chars, recommended: 50-60)")
            elif title_length > 60:
                analysis.append(f"Title tag is too long ({title_length} chars, recommended: 50-60)")
            else:
                analysis.append(f"Title tag length is optimal ({title_length} chars)")
        else:
            analysis.append("Missing title tag")

        # Meta description analysis
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_length = len(meta_desc['content'])
            if desc_length < 120:
                analysis.append(f"Meta description is too short ({desc_length} chars, recommended: 120-155)")
            elif desc_length > 155:
                analysis.append(f"Meta description is too long ({desc_length} chars, recommended: 120-155)")
            else:
                analysis.append(f"Meta description length is optimal ({desc_length} chars)")
        else:
            analysis.append("Missing meta description")

        # Check robots meta tag
        robots = soup.find('meta', {'name': 'robots'})
        if robots:
            analysis.append(f"Robots meta tag found: {robots.get('content', '')}")
        else:
            analysis.append("No robots meta tag found")

        # Check canonical URL
        canonical = soup.find('link', {'rel': 'canonical'})
        if canonical:
            analysis.append(f"Canonical URL is set to: {canonical.get('href', '')}")
        else:
            analysis.append("No canonical URL specified")

        # Check viewport
        viewport = soup.find('meta', {'name': 'viewport'})
        if viewport:
            analysis.append("Viewport meta tag is properly set for mobile devices")
        else:
            analysis.append("Missing viewport meta tag for mobile responsiveness")

        # Check Open Graph tags
        og_tags = soup.find_all('meta', property=re.compile('^og:'))
        if og_tags:
            analysis.append(f"Found {len(og_tags)} Open Graph tags for social media sharing")
        else:
            analysis.append("No Open Graph tags found for social media optimization")

        return analysis

    def analyze_content(self, soup, text_content) -> List[str]:
        """Enhanced content analysis"""
        analysis = []

        # Heading structure analysis
        headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        if headings['h1'] == 0:
            analysis.append("Missing H1 heading (main title)")
        elif headings['h1'] > 1:
            analysis.append(f"Multiple H1 headings detected ({headings['h1']} found, recommended: 1)")

        # Detailed heading structure
        analysis.append(f"Heading structure: {', '.join(f'{k}: {v}' for k, v in headings.items() if v > 0)}")

        # Image analysis
        images = soup.find_all('img')
        total_images = len(images)
        images_without_alt = len([img for img in images if not img.get('alt')])
        large_images = len([img for img in images if img.get('src', '').endswith(('.png', '.jpg', '.jpeg'))])

        analysis.append(f"Total images: {total_images}")
        if images_without_alt > 0:
            analysis.append(f"Images without alt text: {images_without_alt}")
        if large_images > 0:
            analysis.append(f"Consider optimizing {large_images} large image(s)")

        # Content analysis
        if text_content:
            words = text_content.split()
            word_count = len(words)

            # Word count analysis
            if word_count < 300:
                analysis.append(f"Content is too short ({word_count} words, recommended: minimum 300)")
            else:
                analysis.append(f"Good content length: {word_count} words")

            # Keyword density
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Skip short words
                    word = word.lower()
                    word_freq[word] = word_freq.get(word, 0) + 1

            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            analysis.append("Top 5 keywords and their density:")
            for word, count in top_keywords:
                density = (count / word_count) * 100
                analysis.append(f"- '{word}': {density:.1f}% ({count} occurrences)")

        return analysis

    def analyze_technical(self, response, soup) -> List[str]:
        """Enhanced technical analysis"""
        analysis = []

        # Response headers analysis
        headers = response.headers

        # Server information
        server = headers.get('Server', 'Not disclosed')
        analysis.append(f"Server: {server}")

        # Compression
        if 'gzip' in headers.get('Content-Encoding', '').lower():
            analysis.append("Content compression (gzip) is enabled")
        else:
            analysis.append("Content compression is not enabled")

        # Caching headers
        cache_control = headers.get('Cache-Control', 'Not set')
        expires = headers.get('Expires', 'Not set')
        analysis.append(f"Cache-Control: {cache_control}")
        analysis.append(f"Expires: {expires}")

        # Content type and charset
        content_type = headers.get('Content-Type', 'Not set')
        analysis.append(f"Content-Type: {content_type}")

        # URL structure
        parsed_url = urlparse(self.url)
        path_depth = len([x for x in parsed_url.path.split('/') if x])
        if path_depth > 3:
            analysis.append(f"URL structure is deep ({path_depth} levels, recommended: maximum 3)")

        # Mobile optimization
        viewport_meta = soup.find('meta', {'name': 'viewport'})
        if viewport_meta:
            content = viewport_meta.get('content', '')
            if 'width=device-width' in content and 'initial-scale=1' in content:
                analysis.append("Viewport is properly configured for mobile devices")
            else:
                analysis.append("Viewport meta tag needs optimization")

        return analysis

    def analyze_speed(self, response) -> List[str]:
        """Analyze loading speed metrics"""
        analysis = []

        # Response time
        response_time = response.elapsed.total_seconds()
        if response_time > 2:
            analysis.append(f"Slow server response time: {response_time:.2f}s (recommended: < 2s)")
        else:
            analysis.append(f"Good server response time: {response_time:.2f}s")

        # Page size
        content_length = int(response.headers.get('content-length', 0))
        if content_length > 0:
            size_mb = content_length / (1024 * 1024)
            if size_mb > 3:
                analysis.append(f"Large page size: {size_mb:.2f}MB (recommended: < 3MB)")
            else:
                analysis.append(f"Good page size: {size_mb:.2f}MB")

        return analysis

    def analyze_security(self) -> List[str]:
        """Analyze security aspects"""
        analysis = []

        # SSL/HTTPS check
        if self.url.startswith('https'):
            analysis.append("Website is secured with HTTPS")
        else:
            analysis.append("Website is not using HTTPS (security risk)")

        # Domain registration info
        try:
            domain = urlparse(self.url).netloc
            domain_info = whois.whois(domain)

            if domain_info.creation_date:
                creation_date = domain_info.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                age = (datetime.now() - creation_date).days
                analysis.append(f"Domain age: {age} days")

            if domain_info.expiration_date:
                expiration_date = domain_info.expiration_date
                if isinstance(expiration_date, list):
                    expiration_date = expiration_date[0]
                days_until_expiry = (expiration_date - datetime.now()).days
                analysis.append(f"Days until domain expiry: {days_until_expiry}")
        except:
            analysis.append("Could not fetch domain registration information")

        return analysis

    def analyze_links(self, soup) -> List[str]:
        """Analyze internal and external links"""
        analysis = []

        links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        broken_links = []

        base_domain = urlparse(self.url).netloc

        for link in links:
            href = link.get('href')
            if not href or href.startswith('#'):
                continue

            absolute_url = urljoin(self.url, href)
            parsed_url = urlparse(absolute_url)

            if parsed_url.netloc == base_domain or not parsed_url.netloc:
                internal_links.append(absolute_url)
            else:
                external_links.append(absolute_url)

        analysis.append(f"Total links found: {len(links)}")
        analysis.append(f"Internal links: {len(internal_links)}")
        analysis.append(f"External links: {len(external_links)}")

        # Check for nofollow attributes
        nofollow_links = len(soup.find_all('a', rel='nofollow'))
        if nofollow_links > 0:
            analysis.append(f"Links with nofollow: {nofollow_links}")

        return analysis

    def check_mobile_friendly(self) -> bool:
        """Enhanced mobile-friendly check"""
        try:
            response = requests.get(self.url, headers={
                **self.headers,
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
            })
            return response.status_code == 200
        except:
            return False

    def calculate_scores(self, meta_analysis, content_analysis, technical_analysis,
                        speed_analysis, security_analysis, link_analysis) -> Dict[str, float]:
        """Enhanced scoring system"""

        def count_issues(analysis: List[str], keywords: List[str]) -> int:
            return len([x for x in analysis if any(k in x.lower() for k in keywords)])

        # Calculate individual scores
        meta_score = 100 - (count_issues(meta_analysis, ['missing', 'too', 'no']) * 15)
        content_score = 100 - (count_issues(content_analysis, ['missing', 'too short', 'multiple']) * 10)
        technical_score = 100 - (count_issues(technical_analysis, ['not', 'slow', 'needs']) * 20)
        speed_score = 100 - (count_issues(speed_analysis, ['slow', 'large']) * 25)
        security_score = 100 - (count_issues(security_analysis, ['not', 'risk', 'could not']) * 30)
        link_score = 100 - (count_issues(link_analysis, ['broken', 'invalid']) * 15)

        # Normalize scores to 0-100 range
        scores = {
            'meta': max(0, min(100, meta_score)),
            'content': max(0, min(100, content_score)),
            'technical': max(0, min(100, technical_score)),
            'speed': max(0, min(100, speed_score)),
            'security': max(0, min(100, security_score)),
            'links': max(0, min(100, link_score))
        }

        # Calculate weighted overall score
        weights = {
            'meta': 0.2,
            'content': 0.25,
            'technical': 0.15,
            'speed': 0.15,
            'security': 0.15,
            'links': 0.1
        }

        overall_score = sum(scores[k] * weights[k] for k in scores)
        scores['overall'] = max(0, min(100, overall_score))

        return scores

    def generate_improvements(self, meta_analysis, content_analysis, technical_analysis,
                            speed_analysis, security_analysis, link_analysis) -> List[str]:
        """Generate comprehensive improvement suggestions"""
        improvements = []

        # Collect all analyses
        all_analyses = {
            'Meta Tags': meta_analysis,
            'Content': content_analysis,
            'Technical': technical_analysis,
            'Speed': speed_analysis,
            'Security': security_analysis,
            'Links': link_analysis
        }

        # Keywords indicating issues
        issue_keywords = ['missing', 'too', 'no', 'not', 'slow', 'large', 'multiple', 'broken']

        # Generate improvements for each category
        for category, analysis in all_analyses.items():
            for issue in analysis:
                if any(keyword in issue.lower() for keyword in issue_keywords):
                    suggestion = issue
                    suggestion = suggestion.replace('Missing', 'Add')
                    suggestion = suggestion.replace('Too short', 'Increase length of')
                    suggestion = suggestion.replace('Too long', 'Reduce length of')
                    suggestion = suggestion.replace('No ', 'Add ')
                    suggestion = suggestion.replace('Not ', 'Enable ')
                    improvements.append(f"[{category}] {suggestion}")

        return improvements