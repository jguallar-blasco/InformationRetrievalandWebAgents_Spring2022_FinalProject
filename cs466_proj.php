<head><title>Query Output</title></head>
<body>
<?php

   // Alexandra Szewc
   // Jimena Guallar-Blasco

	// collect the posted value in a variable called $item
	$item = $_POST['query'];

	echo "Tweet Queried: ";

	if (!empty($item)) {
		echo $item;
		echo "<br><br>";

		$output = shell_exec("source env6/bin/activate 2>&1");

		$pyrun = "./env6/bin/python3 /home/aszewc1/public_html/cs466/classifier.py --train input_data-train.tsv --test '".$item."' 2>&1";
		$output = shell_exec($pyrun);
		
		echo "<pre>$output</pre>";

   	} else {
      		echo "not set";
	}

?>
</body>
