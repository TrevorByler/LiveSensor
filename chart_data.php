<?php
    $servername = "localhost";   
    $username = "root";
    $password = "logic";
    $dbName = "LightData";
    $conn = new mysqli($servername, $username, $password, $dbName);
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
     
    $query = "SELECT DATE_FORMAT(time, '%Y-%m-%d %H:%i:%s') \"time\", visible_light\n".
		"FROM raw_data\n".
		"WHERE time >= CURRENT_TIMESTAMP - INTERVAL 5 MINUTE";
		
    $result = $conn->query($query);
    if (!$result) {
		trigger_error('Invalid query: ' .$conn->error);
	}
	
    //initialize the array to store the processed data
    $jsonArray = array();
    //check if there is any data returned by the SQL Query
    if ($result->num_rows > 0) {
      //Converting the results into an associative array
      while($row = $result->fetch_assoc()) {
        $jsonArrayItem = array();
        $jsonArrayItem['label'] = $row['time'];
        $jsonArrayItem['value'] = $row['visible_light'];
        //append the above created object into the main array.
        array_push($jsonArray, $jsonArrayItem);
      }
    }
    //Closing the connection to DB
    $conn->close();
    //set the response content type as JSON
    header('Content-type: application/json');
    //output the return value of json encode using the echo function.
    echo json_encode($jsonArray);
?>
