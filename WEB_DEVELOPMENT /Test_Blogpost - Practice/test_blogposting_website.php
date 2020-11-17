<?php
    include('includes/head.php');
    include('includes/post.php');
?>

    <div class="container">

      <div class="blog-header">
        <h1 class="blog-title">Test Bootstrap Blog</h1>
        <p class="lead blog-description">Example Template</p>
      </div>

      <div class="row">

        <div class="col-sm-8 blog-main">

        <?php foreach( $posts as $post ) { ?>
            
          <div class="blog-post">
            <h2 class="blog-post-title"><?php echo $post["post-title"]; ?></h2>
            <p class="blog-post-meta"><?php echo $post["post-date"]; ?> by <a href="#"><?php echo $post["post-author"]; ?></a></p>

              <?php echo $post["post-content"]; ?>
            
          </div>
        <?php } ?>
            
          <nav>
            <ul class="pager">
              <li><a href="#">Prev Page</a></li>
              <li><a href="#">Next Page</a></li>
            </ul>
          </nav>

        </div>
          
        <div class="col-sm-3 col-sm-offset-1 blog-sidebar">
          <?php include('includes/sidebars.php'); ?>
        </div>
      </div>

    </div>

<?php include('includes/foot.php'); ?>