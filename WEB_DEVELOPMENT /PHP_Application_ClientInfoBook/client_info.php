<?php
session_start();

if( !$_SESSION['loggedInUser'] ) {
    
    header("Location: login_page.php");
}

include('includes/db_conn.php');

$query = "SELECT * FROM clients";
$result = mysqli_query( $conn, $query );

if( isset( $_GET['alert'] ) ) {
    
    if( $_GET['alert'] == 'success' ) {
        $alertMessage = "<div class='alert alert-success'>New client information added! <a class='close' data-dismiss='alert'>&times;</a></div>";
        
    } elseif( $_GET['alert'] == 'updatesuccess' ) {
        $alertMessage = "<div class='alert alert-success'>Client information updated! <a class='close' data-dismiss='alert'>&times;</a></div>";
    
    } elseif( $_GET['alert'] == 'deleted' ) {
        $alertMessage = "<div class='alert alert-success'>Client information deleted! <a class='close' data-dismiss='alert'>&times;</a></div>";
    }
      
}

mysqli_close($conn);

include('includes/header.php');
?>

<h1>Client Information Centre</h1>

<?php echo $alertMessage; ?>

<table class="table table-striped table-bordered">
    <tr>
        <th>Client Name</th>
        <th>Client Email ID</th>
        <th>Client Phone Number</th>
        <th>Client Address</th>
        <th>Client Company</th>
        <th>Client-specific Notes</th>
        <th>Edit Information</th>
    </tr>
    
    <?php
    
    if( mysqli_num_rows($result) > 0 ) {
        
        
        while( $row = mysqli_fetch_assoc($result) ) {
            echo "<tr>";
            
            echo "<td>" . $row['name'] . "</td><td>" . $row['email'] . "</td><td>" . $row['phone'] . "</td><td>" . $row['address'] . "</td><td>" . $row['company'] . "</td><td>" . $row['notes'] . "</td>";
            
            echo '<td><a href="edit.php?id=' . $row['id'] . '" type="button" class="btn btn-primary btn-sm">
                    <span class="glyphicon glyphicon-edit"></span>
                    </a></td>';
            
            echo "</tr>";
        }
    } else { 
        echo "<div class='alert alert-warning'>No Client Information availabale.</div>";
    }

    mysqli_close($conn);

    ?>

    <tr>
        <td colspan="7"><div class="text-center"><a href="add.php" type="button" class="btn btn-sm btn-success"><span class="glyphicon glyphicon-plus"></span> Add Client</a></div></td>
    </tr>
</table>

<?php
include('includes/footer.php');
?>