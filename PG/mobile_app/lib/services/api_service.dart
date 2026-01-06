import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

// import 'dart:io'; // Not supported on Web
import 'package:flutter/foundation.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator, localhost for Windows/iOS simulator
  static String get baseUrl {
    if (kReleaseMode) {
      return 'https://livinpg-backend.onrender.com'; // Production URL
    }
    if (kIsWeb) return 'http://127.0.0.1:8000';
    if (defaultTargetPlatform == TargetPlatform.android) {
        // Use local IP for physical device testing
        return 'http://192.168.31.215:8000';
    }
    return 'http://127.0.0.1:8000';
  }
  
  final storage = const FlutterSecureStorage();

  Future<Map<String, dynamic>> login(String email, String password) async {
    final url = Uri.parse('$baseUrl/users/login');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await storage.write(key: 'access_token', value: data['access_token']);
        await storage.write(key: 'user_role', value: data['role']);
        await storage.write(key: 'full_name', value: data['full_name']); // Added
        return data;
      } else {
        throw Exception('Login failed: ${response.body}');
      }
    } catch (e) {
      throw Exception('Error connecting to server: $e');
    }
  }

  Future<String?> getToken() async {
    return await storage.read(key: 'access_token');
  }

  Future<String> getFullName() async {
    return await storage.read(key: 'full_name') ?? 'User';
  }

  Future<List<dynamic>> getMyComplaints() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/complaints/my');
    
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load complaints');
    }
  }

  Future<void> createComplaint(String category, String description) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/complaints/');
    
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'category': category,
        'description': description,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to create complaint: ${response.body}');
    }
  }

  Future<List<dynamic>> getFoodMenu() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/food/');
    
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load food menu');
    }
  }

  // --- Payment Methods ---
  
  Future<List<dynamic>> getMyPayments() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/payments/my');
    
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load payments');
    }
  }

  Future<void> createPayment(int amount, String transactionId) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/payments');
    
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'amount': amount,
        'transaction_id': transactionId,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Payment failed: ${response.body}');
    }
  }

  Future<void> updateFoodMenu(String day, String breakfast, String lunch, String dinner) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/food/');
    
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'day': day,
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update menu: ${response.body}');
    }
  }

  Future<void> register(String fullName, String email, String password, String phone) async {
    final url = Uri.parse('$baseUrl/users/register');
    
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'full_name': fullName,
        'email': email,
        'password': password,
        'phone': phone,
        'role': 'resident' // Default to resident registration
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Registration failed: ${response.body}');
    }
  }

  // --- Admin Methods ---

  Future<Map<String, dynamic>> getStats() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/stats');
    
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load stats');
    }
  }

  Future<List<dynamic>> getAdminComplaints() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/complaints/all');
    
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load complaints');
    }
  }

  Future<void> resolveComplaint(int id) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/complaints/$id/resolve');
    
    final response = await http.put(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to resolve complaint');
    }
  }

  Future<List<dynamic>> getResidents() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/users/residents');
    
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load residents');
    }
  }

  Future<void> deleteUser(int id) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/users/$id');
    
    final response = await http.delete(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to delete user (${response.statusCode}): ${response.body}');
    }
  }

  Future<List<dynamic>> getAllPayments() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/payments');
    
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load all payments');
    }
  }

  Future<void> approvePayment(int id) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/payments/$id/approve');
    
    final response = await http.put(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to approve payment');
    }
  }

  // QR upload temporarily handled manually

  // --- New Features (Improvements) ---

  Future<void> resetPassword(String email, String newPassword) async {
    final url = Uri.parse('$baseUrl/users/reset-password');
    final response = await http.put(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'new_password': newPassword}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to reset password: ${response.body}');
    }
  }

  Future<void> leavePG() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/users/leave');
    final response = await http.post(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to leave PG: ${response.body}');
    }
  }

  Future<List<dynamic>> getRevenue() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/payments/revenue');
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load revenue');
    }
  }
}
