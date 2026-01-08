import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({super.key});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  final ApiService _apiService = ApiService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Notifications"),
        // actions: [] // Removed actions as requested
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
            try {
              await _apiService.clearAllNotifications();
              setState(() {});
            } catch (e) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
            }
        },
        label: const Text("Clear All"),
        icon: const Icon(Icons.delete_sweep),
        backgroundColor: Colors.redAccent,
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _apiService.getMyNotifications(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final notifications = snapshot.data ?? [];
          
          if (notifications.isEmpty) {
             return const Center(child: Text("No notifications"));
          }

          return ListView.builder(
            itemCount: notifications.length,
            itemBuilder: (context, index) {
              final notif = notifications[index];
              return Card(
                color: notif['is_read'] ? Colors.white : Colors.blue[50],
                child: ListTile(
                  leading: Icon(
                    Icons.notifications, 
                    color: notif['type'] == 'payment' ? Colors.green : Colors.blue
                  ),
                  title: Text(notif['title'], style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text(notif['message']),
                  trailing: notif['is_read'] ? null : const Icon(Icons.circle, size: 10, color: Colors.blue),
                  onTap: () async {
                    if (!notif['is_read']) {
                      await _apiService.markNotificationRead(notif['id']);
                      setState(() {});
                    }
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}
