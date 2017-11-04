<?php
if( file_exists(__DIR__.'/github-auth-config.php') ){
    require(__DIR__.'/github-auth-config.php');
}else{
    exit('local github auth config required!');
}

require(__DIR__.'/github-auth-class.php');
$auth = new githubAuth();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0">
    <title>Github login test</title>
    <meta name="keywords" content="keywords"/>
    <meta name="description" content="description"/>
    <style type="text/css">
        .login-box{font-family: Sans-serif;font-size: 24px;}
        .user-profile small{display: block; font-size: 14px;float: right;cursor: pointer;}
        .user-profile pre{background: #ccc;border-radius: 5px;padding: 10px;}
    </style>
</head>
<body>

<?php if($auth->loggedIn()): ?>
    <div class="user-profile">
        <h2>
            You are logged in with github
            <small><a href="?act=logout">logout</a></small>
        </h2>
        <h3>User Info</h3>
        <pre>
            <?php print_r($auth->userInfo()); ?>
        </pre>

        <h3>Session</h3>
        <pre>
            <?php print_r($_SESSION);?>
        </pre>
    </div>
<?php else: ?>
    <div class="login-box">
        <h3>You are not logged in</h3>
        <h2><a href="?act=login"><button type="button">github login</button></a></h2>
    </div>
<?php endif; ?>

</body>
</html>
