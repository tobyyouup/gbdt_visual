<?php
if ($_FILES["file"]["error"] > 0)
{
    echo "Return Code: " . $_FILES["file"]["error"] . "<br />";
}
else
{
    echo "Upload: " . $_FILES["file"]["name"] . "<br />";
    echo "Type: " . $_FILES["file"]["type"] . "<br />";
    echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
    echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";

    $md5 = md5_file($_FILES["file"]["tmp_name"])."--".md5(time().mt_rand(1,1000000));
    echo '#####'.$md5.'#####';
     
    move_uploaded_file($_FILES["file"]["tmp_name"], "model_file/" . $md5);
    echo "Stored in: " . "model_file/" . $md5;
}

?>
