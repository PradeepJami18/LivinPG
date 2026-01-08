import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'features/auth/login_screen.dart';
import 'features/auth/register_screen.dart';
import 'features/resident/dashboard_screen.dart';
import 'features/admin/admin_dashboard.dart';
import 'features/complaints/complaints_list_screen.dart';
import 'features/complaints/create_complaint_screen.dart';
import 'features/food/food_menu_screen.dart';



void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final storage = const FlutterSecureStorage();
  Widget? _homeScreen;

  @override
  void initState() {
    super.initState();
    _checkLoginStatus();
  }

  Future<void> _checkLoginStatus() async {
    final token = await storage.read(key: 'access_token');
    final role = await storage.read(key: 'user_role');

    setState(() {
      if (token != null && role != null) {
        if (role == 'admin') {
          _homeScreen = const AdminDashboard();
        } else {
          _homeScreen = const ResidentDashboard();
        }
      } else {
        _homeScreen = const LoginScreen();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_homeScreen == null) {
       // Show a loading screen while checking storage
       return const MaterialApp(
         debugShowCheckedModeBanner: false,
         home: Scaffold(body: Center(child: CircularProgressIndicator())),
       );
    }

    return MaterialApp(
      title: 'Smart PG Living',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        useMaterial3: true,
      ),
      home: _homeScreen, // Dynamic Home
      routes: {
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/resident_dashboard': (context) => const ResidentDashboard(),
        '/admin_dashboard': (context) => const AdminDashboard(),
        '/my_complaints': (context) => const ComplaintsListScreen(),
        '/create_complaint': (context) => const CreateComplaintScreen(),
        '/food_menu': (context) => const FoodMenuScreen(),
      },
    );
  }
}
