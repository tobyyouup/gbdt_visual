<?php 
@header('Content-type: text/html;charset=utf-8');
ini_set('date.timezone','Asia/Shanghai');

@$model=$_GET['model_file'];
@$sample=$_GET['sample_file'];

//$timeStamp= date('Y-m-d H:i:s',time());

$model = strval($model);
$sample = strval($sample);

exec("python ./gbdt_visual/Sinbad/visual.py \"$model\" \"$sample\"", $ret, $stat);

$result ='';
if ($stat == 0){
     $score='';
     
     for($i = 0;$i<count($ret);$i++){
     	if($i==0){
	    $score = $ret[$i];
	}
	else{
            $score = $score.'#'.$ret[$i];
	}
     }
}
echo $score;

?> 
