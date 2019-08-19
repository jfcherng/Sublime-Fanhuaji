<?php

require __DIR__ . '/ZhConversion.php';

use MediaWiki\Languages\Data\ZhConversion;

$modes = [
    'zh2Hant',
    'zh2Hans',
    'zh2TW',
    'zh2HK',
    'zh2CN',
];

$jsonFlags = \JSON_UNESCAPED_UNICODE | \JSON_PRETTY_PRINT;

foreach ($modes as $mode) {
    $success = \file_put_contents(
        __DIR__ . "/{$mode}.json",
        \json_encode(ZhConversion::$$mode, $jsonFlags)
    );

    if ($success) {
        echo "Done: {$mode}", PHP_EOL;
    }
}
