import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscure = true;
  bool _isLoading = false;

  final Color orange = const Color(0xFFEA580C);
  final Color dark = const Color(0xFF374151);
  final Color sub = const Color(0xFF4B5563);
  
  final _apiService = ApiService();

  void _showResetDialog() {
    final emailCtrl = TextEditingController();
    final passCtrl = TextEditingController();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Reset Password'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: emailCtrl, decoration: const InputDecoration(labelText: 'Email')),
            TextField(controller: passCtrl, decoration: const InputDecoration(labelText: 'New Password'), obscureText: true),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () async {
              try {
                await _apiService.resetPassword(emailCtrl.text, passCtrl.text);
                if (!mounted) return;
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Password Reset Successfully')));
              } catch (e) {
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
              }
            },
            child: const Text('Reset'),
          ),
        ],
      ),
    );
  }

  Future<void> _handleLogin() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter both email and password')),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final response = await _apiService.login(email, password);
      
      if (!mounted) return;

      final role = response['role'];
      
      if (role == 'admin') {
        Navigator.pushReplacementNamed(context, '/admin_dashboard');
      } else {
        Navigator.pushReplacementNamed(context, '/resident_dashboard');
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString().replaceAll('Exception: ', ''))),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [

          /// 🔶 BIG TOP ILLUSTRATION (HOUSE + CURVE)
          Positioned(
            top: 40,
            left: 0,
            right: 0,
            child: Image.asset(
              'assets/images/logo.png', // 👈 USE THIS IMAGE
              width: size.width * 0.9,
              fit: BoxFit.contain,
            ),
          ),

          /// 🔶 FORM CONTENT (OVERLAPS CURVE)
          Positioned(
            top: size.height * 0.32, // Reduced from 0.38 to close gap
            left: 0,
            right: 0,
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 380),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [

                      /// TITLE
                      Text(
                        'LIVINPG',
                        style: TextStyle(
                          fontSize: 30,
                          fontWeight: FontWeight.w800,
                          color: orange,
                        ),
                      ),

                      const SizedBox(height: 6),

                      Text(
                        'Welcome back! Please login.',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                          color: sub,
                        ),
                      ),

                      const SizedBox(height: 24),

                      /// EMAIL
                      _label('Email'),
                      _input(
                        controller: _emailController,
                        hint: 'resident@example.com',
                      ),

                      const SizedBox(height: 12),

                      /// PASSWORD
                      _label('Password'),
                      _passwordField(),

                      const SizedBox(height: 18),

                      /// FORGOT + LOGIN
                      Row(
                        children: [
                          Expanded(
                            child: TextButton(
                              onPressed: _showResetDialog,
                              child: Text(
                                'Forget Password?',
                                style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600,
                                  color: dark,
                                ),
                              ),
                            ),
                          ),
                          SizedBox(
                            height: 32,
                            child: ElevatedButton(
                              onPressed: _isLoading ? null : _handleLogin,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: orange,
                                padding: const EdgeInsets.symmetric(horizontal: 18),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(6),
                                ),
                              ),
                              child: _isLoading 
                                ? SizedBox(
                                    width: 16, 
                                    height: 16, 
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2, 
                                      color: Colors.white
                                    )
                                  )
                                : const Text(
                                'Login ➜',
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: 14),

                      /// CREATE ACCOUNT
                      SizedBox(
                        width: double.infinity,
                        height: 36,
                        child: OutlinedButton(
                          onPressed: () {
                             Navigator.pushNamed(context, '/register');
                          },
                          style: OutlinedButton.styleFrom(
                            side: BorderSide(color: orange.withOpacity(0.5)),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(6),
                            ),
                          ),
                          child: Text(
                            'Create New Account',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                              color: dark,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// ---------------- UI HELPERS ----------------

  Widget _label(String text) => Padding(
        padding: const EdgeInsets.only(bottom: 4),
        child: Align(
          alignment: Alignment.centerLeft,
          child: Text(
            text,
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w700,
              color: dark,
            ),
          ),
        ),
      );

  Widget _input({
    required TextEditingController controller,
    required String hint,
  }) =>
      SizedBox(
        height: 35,
        child: TextField(
          controller: controller,
          style: const TextStyle(fontSize: 14),
          decoration: InputDecoration(
            hintText: hint,
            isDense: true,
            contentPadding:
                const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: orange),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: orange, width: 2),
            ),
          ),
        ),
      );

  Widget _passwordField() => SizedBox(
        height: 35,
        child: TextField(
          controller: _passwordController,
          obscureText: _obscure,
          style: const TextStyle(fontSize: 14),
          decoration: InputDecoration(
            isDense: true,
            contentPadding:
                const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: orange),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(6),
              borderSide: BorderSide(color: orange, width: 2),
            ),
            suffixIcon: IconButton(
              icon: Icon(
                _obscure ? Icons.visibility_off : Icons.visibility,
                size: 18,
                color: dark,
              ),
              onPressed: () => setState(() => _obscure = !_obscure),
            ),
          ),
        ),
      );
}
