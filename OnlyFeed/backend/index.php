<?php 

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include 'conf.php';

$db_conn = (pg_connect("host=".$SERVER.
					   " dbname=".$DB.
					   " user=".$USERNAME. 
					   " password=".$PASSWORD
		   ))or die('Connexion impossible : ' . pg_last_error());

print(pg_connection_status($db_conn));

//$query = 'SELECT * FROM "chatbot_user"';
//$result = pg_query($query) or die('Échec de la requête : ' . pg_last_error());

?>