<?php
$content =  file_get_contents("gbdt_visual/relevanceModelXG_raw.all");
$str = str_replace("\n", "<br />",str_replace("\r","<br />",$content));
echo $str;
//echo $content;
?>
