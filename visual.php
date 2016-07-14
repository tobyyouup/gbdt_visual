<?php 
@header('Content-type: text/html;charset=utf-8');
ini_set('date.timezone','Asia/Shanghai');

@$model=$_GET['model_file'];
@$feature=$_GET['feature_file'];
@$sample=$_GET['sample_file'];

//$timeStamp= date('Y-m-d H:i:s',time());

if ($model == ''){
exec("python ./gbdt_visual/visual.py", $ret, $stat);

}
else{
exec("python ./gbdt_visual/visual.py $model $feature $sample", $ret, $stat);

}

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
     $score = $score.'##';
     echo $score;   
     for($i =0;$i<100;$i++){
	if($model==''){
     		$result= $result.'tree'.$i.'<p style="text-align:center;"><img src="png/default/tree'.$i.'.png" width="100%"/></p> <br />';
	}
	else{
     		$result= $result.'tree'.$i.'<p style="text-align:center;"><img src="png/'.$model.'/tree'.$i.'.png" width="100%"/></p> <br />';
	
	}
     }
}
echo $result;

?> 
