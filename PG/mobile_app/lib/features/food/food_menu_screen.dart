import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class FoodMenuScreen extends StatefulWidget {
  const FoodMenuScreen({super.key});

  @override
  State<FoodMenuScreen> createState() => _FoodMenuScreenState();
}

class _FoodMenuScreenState extends State<FoodMenuScreen> {
  final _apiService = ApiService();
  late Future<List<dynamic>> _menuFuture;

  @override
  void initState() {
    super.initState();
    _menuFuture = _apiService.getFoodMenu();
  }

  Future<void> _refreshMenu() async {
    setState(() {
      _menuFuture = _apiService.getFoodMenu();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Weekly Food Menu'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _menuFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No menu available'));
          }

          final menuItems = snapshot.data!;
          // Sort presumably by day if we wanted, but API returns list.
          
          return RefreshIndicator(
            onRefresh: _refreshMenu,
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: menuItems.length,
              itemBuilder: (context, index) {
                final item = menuItems[index];
                return Card(
                  elevation: 3,
                  margin: const EdgeInsets.only(bottom: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.calendar_today, color: Colors.deepOrange),
                            const SizedBox(width: 8),
                            Text(
                              item['day'] ?? 'Unknown Day',
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.deepOrange,
                              ),
                            ),
                          ],
                        ),
                        const Divider(height: 24),
                        _buildMealRow(Icons.wb_sunny_outlined, 'Breakfast', item['breakfast']),
                        const SizedBox(height: 12),
                        _buildMealRow(Icons.wb_sunny, 'Lunch', item['lunch']),
                        const SizedBox(height: 12),
                        _buildMealRow(Icons.nights_stay, 'Dinner', item['dinner']),
                      ],
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }

  Widget _buildMealRow(IconData icon, String label, String? value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 20, color: Colors.grey[700]),
        const SizedBox(width: 12),
        SizedBox(
          width: 80,
          child: Text(
            label,
            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
          ),
        ),
        Expanded(
          child: Text(
            value ?? 'Not set',
            style: const TextStyle(fontSize: 16),
          ),
        ),
      ],
    );
  }
}
