<?php
$content =  file_get_contents("eg/sample.text");
$str = str_replace("\n", "<br />",str_replace("\r","<br />",$content));
echo $str;
//echo $content;
?>
