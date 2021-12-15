<?php 

session_start();
include "global_variables_for_db.php";

    
   
$error='';

if(isset($_POST['submit'])){
    if (empty($_POST['username']) || empty($_POST['password'])) {
        $error = "Incorrect";
    }
    else {
        $username=$_POST['username'];
        $password=$_POST['password'];
        
        $query = mysqli_query($conn, "SELECT * FROM loginform WHERE username= '$username' AND password = '$password'");
        
        //$rows = mysqli_num_rows($query);
        
        if(mysqli_num_rows($query) >0){
            $rows = mysqli_fetch_array($query);
            $_SESSION['username'] = $rows[1];
            header("Location: index.php");
        }
        else {
            $error = "Invalid";
            ?>
            <script>
                alert("Incorrect username/password");
                window.location.replace("loginform.php");
            </script><?php
            
        }
        mysqli_close($conn);
    }
}
?>