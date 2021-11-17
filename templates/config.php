<?php

$host = "localhost";
$user = "postgres";
$password = "Theknights5!";
$dbname = "MomsMagic";
$con = pg_connect("host=$host dbname=$dbname user=$user password=$password");

if (!$con) {
   die('Connection failed.');
}