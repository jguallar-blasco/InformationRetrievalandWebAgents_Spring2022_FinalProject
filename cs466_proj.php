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

		$pyrun = "./bin/python3 /home/aszewc1/public_html/cs466/classifier.py --train input_data-train.tsv --test '".$item."' 2>&1";

		$output = shell_exec($pyrun);
		echo "<pre>$output</pre>";

		echo $pyrun;
   	} else {
      		echo "not set";
	}

?>
</body>
