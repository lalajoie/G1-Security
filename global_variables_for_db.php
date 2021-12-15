<?php
$ip_server = getHostByName(getHostName());

   if($ip_server == '192.168.1.18'){
       $servername = "localhost";
        $username = "root";
        $password = "";
        $database = "g1security";
   }
    elseif($ip_server == '192.168.1.7'){
        $servername = "localhost";
        $username = "g1sec";
        $password = "lala";
        $database = "g1security";
}
	
	$conn = mysqli_connect($servername, $username, $password, $database);
	// Check connection
	if (!$conn) {
		die("Connection failed: " . mysqli_connect_error());
	}

?>
