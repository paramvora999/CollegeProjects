<?php
session_start();

if( !$_SESSION['loggedInUser'] ) {
    
    // send them to the login page
    header("Location: login_page.php");
}

include('includes/db_conn.php');

include('includes/fn.php');

if( isset( $_POST['add'] ) ) {
    
    $clientName = $clientEmail = $clientPhone = $clientAddress = $clientCompany = $clientNotes = "";
    
    
    if( !$_POST["clientName"] ) {
        $nameError = "Enter name of Client : <br>";
    } else {
        $clientName = validateFormData( $_POST["clientName"] );
    }

    if( !$_POST["clientEmail"] ) {
        $emailError = "Enter Email ID for Client : <br>";
    } else {
        $clientEmail = validateFormData( $_POST["clientEmail"] );
    }
    
    $clientPhone    = validateFormData( $_POST["clientPhone"] );
    $clientAddress  = validateFormData( $_POST["clientAddress"] );
    $clientCompany  = validateFormData( $_POST["clientCompany"] );
    $clientNotes    = validateFormData( $_POST["clientNotes"] );
    
    // if required fields have data
    if( $clientName && $clientEmail ) {
        
        // create query
        $query = "INSERT INTO clients (id, name, email, phone, address, company, notes, date_added) VALUES (NULL, '$clientName', '$clientEmail', '$clientPhone', '$clientAddress', '$clientCompany', '$clientNotes', CURRENT_TIMESTAMP)";
        
        $result = mysqli_query( $conn, $query );
        
        // if query was successful
        if( $result ) {
            
            header( "Location: client_info.php?alert=success" );
        } else {
            
            echo "Error detected !". $query ."<br>" . mysqli_error($conn);
        }
        
    }
    
}

// close the mysql connection
mysqli_close($conn);


include('includes/header.php');
?>

<h1>Add Client Information</h1>

<form action="<?php echo htmlspecialchars( $_SERVER['PHP_SELF'] ); ?>" method="post" class="row">
    <div class="form-group col-sm-6">
        <label for="client-name">Name of Client*</label>
        <input type="text" class="form-control input-lg" id="client-name" name="clientName" value="">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-email">Email ID of Client *</label>
        <input type="text" class="form-control input-lg" id="client-email" name="clientEmail" value="">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-phone">Phone Number of Client *</label>
        <input type="text" class="form-control input-lg" id="client-phone" name="clientPhone" value="">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-address">Address of Client *</label>
        <input type="text" class="form-control input-lg" id="client-address" name="clientAddress" value="">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-company">Company of Client *</label>
        <input type="text" class="form-control input-lg" id="client-company" name="clientCompany" value="">
    </div>
    <div class="form-group col-sm-6">
        <label for="client-notes">Notes (Client specific) *</label>
        <textarea type="text" class="form-control input-lg" id="client-notes" name="clientNotes"></textarea>
    </div>
    <div class="col-sm-12">
            <a href="clients.php" type="button" class="btn btn-lg btn-default">Cancel New Client Information addition </a>
            <button type="submit" class="btn btn-lg btn-success pull-right" name="add">Add New Client</button>
    </div>
</form>

<?php
include('includes/footer.php');
?>