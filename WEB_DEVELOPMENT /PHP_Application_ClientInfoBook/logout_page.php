<?php
if( isset( $_COOKIE[ session_name() ] ) ) {

    setcookie( session_name(), '', time()-86400, '/' );

}

session_unset();

session_destroy();

include('includes/header.php');
?>

<h1>Log Out</h1>

<p class="lead">Log Out successful</p>

<?php
include('includes/footer.php');
?>