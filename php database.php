<?php
// Database connection details
$servername = "localhost";
$username = "your_username";
$password = "your_password";
$dbname = "your_database";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO instalasi (nama, tanggal_instalasi, gambar_asli, gambar_flir, gambar_deteksi) VALUES (?, ?, ?, ?, ?)");
$stmt->bind_param("sssss", $nama, $tanggal_instalasi, $gambar_asli, $gambar_flir, $gambar_deteksi);

// Set parameters and execute
$nama = "Your Installation Name";
$tanggal_instalasi = "2024-03-17"; // or whatever the installation date is
$gambar_asli = "path/to/original/image";
$gambar_flir = "path/to/flir/image";
$gambar_deteksi = "path/to/detection/image";
$stmt->execute();

echo "New records created successfully";

// Close statement and connection
$stmt->close();
$conn->close();
?>
