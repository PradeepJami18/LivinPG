import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import 'package:intl/intl.dart';

class ComplaintsListScreen extends StatefulWidget {
  const ComplaintsListScreen({super.key});

  @override
  State<ComplaintsListScreen> createState() => _ComplaintsListScreenState();
}

class _ComplaintsListScreenState extends State<ComplaintsListScreen> {
  final _apiService = ApiService();
  late Future<List<dynamic>> _complaintsFuture;

  @override
  void initState() {
    super.initState();
    _complaintsFuture = _apiService.getMyComplaints();
  }

  Future<void> _refreshComplaints() async {
    setState(() {
      _complaintsFuture = _apiService.getMyComplaints();
    });
  }

  Color _getStatusColor(String status) {
    switch (status.toLowerCase()) {
      case 'resolved':
        return Colors.green;
      case 'pending':
        return Colors.orange;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Complaints'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _complaintsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No complaints found'));
          }

          final complaints = snapshot.data!;
          return RefreshIndicator(
            onRefresh: _refreshComplaints,
            child: ListView.builder(
              itemCount: complaints.length,
              itemBuilder: (context, index) {
                final complaint = complaints[index];
                final date = DateTime.parse(complaint['created_at']);
                final formattedDate = DateFormat('MMM d, y').format(date);

                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: _getStatusColor(complaint['status']),
                      child: const Icon(Icons.report_problem, color: Colors.white),
                    ),
                    title: Text(complaint['category']),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(complaint['description']),
                        Text(
                          formattedDate,
                          style: const TextStyle(fontSize: 12, color: Colors.grey),
                        ),
                      ],
                    ),
                    trailing: Text(
                      complaint['status'],
                      style: TextStyle(
                        color: _getStatusColor(complaint['status']),
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.pushNamed(context, '/create_complaint').then((_) => _refreshComplaints());
        },
        backgroundColor: Colors.deepOrange,
        child: const Icon(Icons.add, color: Colors.white),
      ),
    );
  }
}
