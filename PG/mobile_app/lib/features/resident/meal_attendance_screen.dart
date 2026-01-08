import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import 'package:intl/intl.dart';

class MealAttendanceScreen extends StatefulWidget {
  const MealAttendanceScreen({super.key});

  @override
  State<MealAttendanceScreen> createState() => _MealAttendanceScreenState();
}

class _MealAttendanceScreenState extends State<MealAttendanceScreen> {
  final ApiService _apiService = ApiService();
  bool _breakfast = true;
  bool _lunch = true;
  bool _dinner = true;
  bool _isLoading = false;

  Future<void> _submitAttendance() async {
    setState(() => _isLoading = true);
    final today = DateFormat('yyyy-MM-dd').format(DateTime.now());
    
    try {
      await _apiService.updateMealAttendance(today, _breakfast, _lunch, _dinner);
      if(!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Preferences Saved!")));
      Navigator.pop(context);
    } catch (e) {
      if(!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Eat Outside / Skip Meal")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text(
              "Intimate PG Owner", 
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)
            ),
            const SizedBox(height: 10),
            const Text("Going to a party or eating outside? Uncheck the meals you will skip today so we don't waste food.", textAlign: TextAlign.center, style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 20),
            
            CheckboxListTile(
              title: const Text("Breakfast"),
              value: !_breakfast, // Inverted logic: Checked = Skipping
              secondary: const Icon(Icons.breakfast_dining),
              onChanged: (val) => setState(() => _breakfast = !val!), // If checked (val=true), breakfast=false
            ),
            CheckboxListTile(
              title: const Text("Lunch"),
              value: !_lunch,
              secondary: const Icon(Icons.lunch_dining),
              onChanged: (val) => setState(() => _lunch = !val!),
            ),
            CheckboxListTile(
              title: const Text("Dinner"),
              value: !_dinner,
              secondary: const Icon(Icons.dinner_dining),
              onChanged: (val) => setState(() => _dinner = !val!),
            ),

            const SizedBox(height: 20),
            
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _submitAttendance,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.deepOrange, 
                  foregroundColor: Colors.white
                ),
                child: _isLoading 
                  ? const CircularProgressIndicator(color: Colors.white) 
                  : const Text("Update Status"),
              ),
            )
          ],
        ),
      ),
    );
  }
}
