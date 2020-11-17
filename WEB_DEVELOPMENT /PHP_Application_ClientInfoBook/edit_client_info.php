<?php
session_start();

if( !$_SESSION['loggedInUser'] ) {
    
    header("Location: login_page.php");
}

$clientID = $_GET['id'];

include('includes/db_conn.php');

include('includes/fn.php');

$query = "SELECT * FROM clients WHERE id='$clientID'";
$result = mysqli_query( $conn, $query );

if( mysqli_num_rows($result) > 0 ) {
    
    while( $row = mysqli_fetch_assoc($result) ) {
        $clientName     = $row['name'];
        $clientEmail    = $row['email'];
        $clientPhone    = $row['phone'];
        $clientAddress  = $row['address'];
        $clientCompany  = $row['company'];
        $clientNotes    = $row['notes'];
    }
} else {
    $alertMessage = "<div class='alert alert-warning'>No client information available.<a href='clients.php'>Head back</a>.</div>";
}

// if update button was submitted
if( isset($_POST['update']) ) {
    
    $clientName     = validateFormData( $_POST["clientName"] );
    $clientEmail    = validateFormData( $_POST["clientEmail"] );
    $clientPhone    = validateFormData( $_POST["clientPhone"] );
    $clientAddress  = validateFormData( $_POST["clientAddress"] );
    $clientCompany  = validateFormData( $_POST["clientCompany"] );
    $clientNotes    = validateFormData( $_POST["clientNotes"] );
    
    $query = "UPDATE clients
            SET name='$clientName',
            email='$clientEmail',
            phone='$clientPhone',
            address='$clientAddress',
            company='$clientCompany',
            notes='$clientNotes'
            WHERE id='$clientID'";
    
    $result = mysqli_query( $conn, $query );
    
    if( $result ) {
        
        header("Location: client_info.php?alert=updatesuccess");
    } else {
        echo "Error updating client record: " . mysqli_error($conn); 
    }
}

if( isset($_POST['delete']) ) {
    
    $alertMessage = "<div class='alert alert-danger'>
                        <p>Delete client information ?</p><br>
                        <form action='". htmlspecialchars( $_SERVER["PHP_SELF"] ) ."?id=$clientID' method='post'>
                            <input type='submit' class='btn btn-danger btn-sm' name='confirm-delete' value='Confirm Deletion'>
                            <a type='button' class='btn btn-default btn-sm' data-dismiss='alert'>Cancel Deletion</a>
                        </form>
                    </div>";
    
}

// if confirm delete button was submitted
if( isset($_POST['confirm-delete']) ) {
    
    // new database query & result
    $query = "DELETE FROM clients WHERE id='$clientID'";
    $result = mysqli_query( $conn, $query );
    
    if( $result ) {
        
        header("Location: client_info.php?alert=deleted");
    } else {
        echo "Error updating record: " . mysqli_error($conn);
    }
    
}

mysqli_close($conn);

include('includes/header.php');
?>

<h1>Edit Client Information</h1>

<?php echo $alertMessage; ?>

<form action="<?php echo htmlspecialchars( $_SERVER['PHP_SELF'] ); ?>?id=<?php echo $clientID; ?>" method="post" class="row">
    <div class="form-group col-sm-6">
        <label for="client-name">Name</label>
        <input type="text" class="form-control input-lg" id="client-name" name="clientName" value="<?php echo $clientName; ?>">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-email">Email</label>
        <input type="text" class="form-control input-lg" id="client-email" name="clientEmail" value="<?php echo $clientEmail; ?>">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-phone">Phone</label>
        <input type="text" class="form-control input-lg" id="client-phone" name="clientPhone" value="<?php echo $clientPhone; ?>">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-address">Address</label>
        <input type="text" class="form-control input-lg" id="client-address" name="clientAddress" value="<?php echo $clientAddress; ?>">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-company">Company</label>
        <input type="text" class="form-control input-lg" id="client-company" name="clientCompany" value="<?php echo $clientCompany; ?>">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-notes">Notes</label>
        <textarea type="text" class="form-control input-lg" id="client-notes" name="clientNotes"><?php echo $clientNotes; ?></textarea>
    </div>
    <div class="col-sm-12">
        <hr>
        <button type="submit" class="btn btn-lg btn-danger pull-left" name="delete">Delete Client Information</button>
        <div class="pull-right">
            <a href="clients.php" type="button" class="btn btn-lg btn-default">Cancel Action</a>
            <button type="submit" class="btn btn-lg btn-success" name="update">Update Client Information</button>
        </div>
    </div>
</form>

<?php
include('includes/footer.php');
?>