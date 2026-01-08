import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import 'package:url_launcher/url_launcher.dart'; // Ensure url_launcher is in pubspec or use intent

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final apiService = ApiService();

    // Profile Dialog with Full Details
    void showProfile() async {
      // Show loading first
      showDialog(context: context, barrierDismissible: false, builder: (c) => const Center(child: CircularProgressIndicator()));
      
      try {
        final profile = await apiService.getMyProfile();
        if(!context.mounted) return;
        Navigator.pop(context); // Pop loading

        showDialog(
          context: context,
          builder: (c) => AlertDialog(
            title: const Text("My Profile"),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: CircleAvatar(
                    radius: 35,
                    backgroundColor: Colors.deepOrange,
                    child: Text(
                      profile['full_name'][0].toUpperCase(),
                      style: const TextStyle(fontSize: 30, color: Colors.white, fontWeight: FontWeight.bold)
                    ),
                  )
                ),
                const SizedBox(height: 16),
                _buildInfoRow(Icons.person, "Name", profile['full_name'] ?? 'N/A'),
                _buildInfoRow(Icons.email, "Email", profile['email'] ?? 'N/A'),
                _buildInfoRow(Icons.phone, "Phone", profile['phone'] ?? 'N/A'),
                _buildInfoRow(Icons.badge, "Role", (profile['role'] ?? 'resident').toString().toUpperCase()),
                _buildInfoRow(Icons.calendar_today, "Joined", (profile['created_at'] ?? DateTime.now().toString()).split('T')[0]),
              ],
            ),
            actions: [TextButton(onPressed: () => Navigator.pop(c), child: const Text("Close"))],
          ),
        );
      } catch (e) {
        if(!context.mounted) return;
        Navigator.pop(context); // Pop loading
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error fetching profile: $e")));
      }
    }

    void emailAdmin() async {
      final Uri emailLaunchUri = Uri(
        scheme: 'mailto',
        path: 'smartlivinpg@gmail.com',
        query: 'subject=Support Request&body=Hi Admin, I need help with...',
      );
        try {
          if (!await launchUrl(emailLaunchUri)) {
            throw 'Could not launch email';
          }
        } catch (e) {
           ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Could not open email app. Write to: smartlivinpg@gmail.com")));
        }
    }

    void callAdmin() async {
      final Uri callUri = Uri(scheme: 'tel', path: '+919876543210'); // Placeholder number
      try {
        if (!await launchUrl(callUri)) {
          throw 'Could not launch dialer';
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Could not open dialer")));
      }
    }

    void logout() async {
      await apiService.storage.deleteAll();
      if (context.mounted) {
         Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
      }
    }

    return Scaffold(
      appBar: AppBar(title: const Text("Settings")),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text("Profile"),
            subtitle: const Text("View your details"),
            onTap: showProfile,
          ),
          const Divider(),
          const Padding(
            padding: EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Text("Support", style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.grey)),
          ),
          ListTile(
            leading: const Icon(Icons.call, color: Colors.green),
            title: const Text("Call Admin"),
            subtitle: const Text("+91 98765 43210"),
            onTap: callAdmin,
          ),
          ListTile(
            leading: const Icon(Icons.email, color: Colors.blue),
            title: const Text("Email Support"),
            subtitle: const Text("smartlivinpg@gmail.com"),
            onTap: emailAdmin,
          ),
          const Divider(),
          const SizedBox(height: 20),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text("Logout", style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
            onTap: logout,
          ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(icon, size: 20, color: Colors.grey),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
                Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
              ],
            ),
          )
        ],
      ),
    );
  }
}
