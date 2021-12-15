<?php
include("loginprocess.php");
?>


<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="fonts/icomoon/style.css">

    <link rel="stylesheet" href="css/owl.carousel.min.css">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    
    <!-- Style -->
    <link rel="stylesheet" href="css/style.css">

    <title></title>
  </head>

  <body>

  
  <div class="content">
    <div class="container">
      <div class="row justify-content-center">
        <!-- <div class="col-md-6 order-md-2">
          <img src="images/undraw_file_sync_ot38.svg" alt="Image" class="img-fluid">
        </div> -->
        <div class="col-md-6 contents">
          <div class="row justify-content-center">
            <div class="col-md-12">
                
                
                
                
                
              <div class="form-block">
                  <div class="mb-4">
                  <h3>Sign In to <strong>G1 Security</strong></h3>
                  </div>
                <form action="loginprocess.php" method="POST">
                  <div class="form-group first">
                    <label for="username">Username</label>
                    <input type="text" id ="username" name="username" class="form-control" required>

                  </div>
                  <div class="form-group last mb-4">
                    <label for="password">Password</label>
                    <input type="password" name="password"  class="form-control" id="password" required>
                    
                  </div>
                
                        <input type ="submit" name ="submit" id = "submit" value = "Log In" class = "btn btn-block btn-primary btn-lg"/>
                  
                </form>
              </div>
            </div>
          </div>
          
        </div>
        
      </div>
    </div>
  </div>

  
    <script src="js/jquery-3.3.1.min.js"></script>
    <script src="js/popper.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/main.js"></script>
    
    
      
      <span><?php echo $error; ?></span>
  </body>
</html>