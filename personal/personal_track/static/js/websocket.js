const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');
// Sunucudan mesaj alındığında tetiklenir
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const message = data.message;

    // Bildirimi göster
    Swal.fire({
        title: 'Geç Kalma Bildirimi',
        text: message,
        icon: 'warning',
        confirmButtonText: 'Tamam'
    });
};

// WebSocket bağlantısı kapandığında tetiklenir