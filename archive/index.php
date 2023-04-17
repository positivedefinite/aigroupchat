<!DOCTYPE html>
<html>
<head>
  <title>Guest Book</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
</head>
<body>

  <div class="container mt-5">
    <h1>Guest Book</h1>
    <hr>

    <form action="" method="post">
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" class="form-control" id="name" name="name" required>
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" class="form-control" id="email" name="email" required>
      </div>
      <div class="form-group">
        <label for="message">Message:</label>
        <textarea class="form-control" id="message" name="message" rows="3" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <?php
      // Create or open the database
      $db = new PDO('sqlite:guestbook.db');

      // Create the table if it doesn't exist yet
      $db->exec('CREATE TABLE IF NOT EXISTS guestbook (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)');

      // If the form was submitted, save the data to the database
      if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $name = $_POST['name'];
        $email = $_POST['email'];
        $message = $_POST['message'];

        $stmt = $db->prepare('INSERT INTO guestbook (name, email, message) VALUES (:name, :email, :message)');
        $stmt->bindParam(':name', $name);
        $stmt->bindParam(':email', $email);
        $stmt->bindParam(':message', $message);
        $stmt->execute();
      }

      // Retrieve the guest book entries from the database
      $stmt = $db->query('SELECT * FROM guestbook ORDER BY created_at DESC');
      $entries = $stmt->fetchAll(PDO::FETCH_ASSOC);

      // Display the entries
      echo '<hr><h2>Entries:</h2>';
      foreach ($entries as $entry) {
        echo '<div class="card mt-3">';
        echo '<div class="card-body">';
        echo '<h5 class="card-title">' . htmlspecialchars($entry['name']) . '</h5>';
        echo '<h6 class="card-subtitle mb-2 text-muted">' . htmlspecialchars($entry['email']) . '</h6>';
        echo '<p class="card-text">' . htmlspecialchars($entry['message']) . '</p>';
        echo '<small class="text-muted">' . htmlspecialchars($entry['created_at']) . '</small>';
        echo '</div>';
        echo '</div>';
      }
    ?>

  </div>

</body>
</html>
