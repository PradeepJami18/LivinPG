import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart'; // For kIsWeb
import 'package:url_launcher/url_launcher.dart';
import '../../services/api_service.dart';
import '../complaints/complaints_list_screen.dart';
import '../food/food_menu_screen.dart';
// import 'package:fl_chart/fl_chart.dart';

class ResidentDashboard extends StatefulWidget {
  const ResidentDashboard({super.key});

  @override
  State<ResidentDashboard> createState() => _ResidentDashboardState();
}

class _ResidentDashboardState extends State<ResidentDashboard> {
  final _apiService = ApiService();
  int _selectedIndex = 0;
  String _userName = 'Resident';

  @override
  void initState() {
    super.initState();
    _loadUserName();
  }

  Future<void> _loadUserName() async {
    final name = await _apiService.getFullName();
    if (mounted) setState(() => _userName = name);
  }

  // --- TAB PAGES ---

  // 1. Home Tab
  Widget _buildHomeTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildWelcomeCard(),
          const SizedBox(height: 24),
          const Text('Quick Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          Row(
            children: [
               Expanded(child: _buildQuickAction(Icons.payment, 'Pay Rent', Colors.green, () => setState(() => _selectedIndex = 1))),
               const SizedBox(width: 16),
               Expanded(child: _buildQuickAction(Icons.report_problem, 'Raise Issue', Colors.orange, () => setState(() => _selectedIndex = 3))),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
               Expanded(child: _buildQuickAction(Icons.restaurant_menu, 'Check Menu', Colors.blue, () => setState(() => _selectedIndex = 2))),
               const SizedBox(width: 16),
               Expanded(child: _buildQuickAction(Icons.exit_to_app, 'Leave PG', Colors.red, _confirmLeavePG)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildWelcomeCard() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [Colors.deepOrange, Colors.orangeAccent]),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.deepOrange.withOpacity(0.3), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: const Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Welcome Back!', style: TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
          SizedBox(height: 8),
          Text('Smart LivinPG', style: TextStyle(color: Colors.white70, fontSize: 16)),
        ],
      ),
    );
  }

  Widget _buildQuickAction(IconData icon, String label, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 100,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 8)],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircleAvatar(backgroundColor: color.withOpacity(0.1), child: Icon(icon, color: color)),
            const SizedBox(height: 8),
            Text(label, style: const TextStyle(fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }

  Future<void> _launchUPI(String amount) async {
    if (amount.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Please enter amount')));
      return;
    }
    // Using a generic UPI intent. Android chooses the app (PhonePe/GPay).
    // Replace 'admin@upi' with real ID if available.
    final upiUrl = 'upi://pay?pa=6300243051-3@ybl&pn=SmartPG&am=$amount&cu=INR';
    final uri = Uri.parse(upiUrl);
    
    if (kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('UPI Deep linking works on Mobile App only. Please scan QR Code.')));
      return;
    }

    try {
      if (!await launchUrl(uri, mode: LaunchMode.externalApplication)) {
        throw 'Could not launch UPI app';
      }
    } catch (e) {
      // On emulator or if no app found
       ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error or No UPI App found: $e')));
    }
  }

  Future<void> _confirmLeavePG() async {
     final confirm = await showDialog<bool>(
       context: context,
       builder: (context) => AlertDialog(
         title: const Text('Leave PG?'),
         content: const Text('Are you sure you want to leave? This will mark your status as "Notice Period" and notify the admin.'),
         actions: [
           TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
           TextButton(
              onPressed: () => Navigator.pop(context, true), 
              style: TextButton.styleFrom(foregroundColor: Colors.red),
              child: const Text('Confirm Leave'),
            ),
         ],
       ),
     );

     if (confirm == true) {
       try {
         await _apiService.leavePG();
         if (!mounted) return;
         ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('We notified admin, admin will contact you')));
       } catch (e) {
         if (!mounted) return;
         ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
       }
     }
  }

  // 2. Payments Tab
  Widget _buildPaymentsTab() {
    final amountController = TextEditingController();
    final txnController = TextEditingController();

    return SingleChildScrollView(
      child: Column(
        children: [
          // Payment Form
          ExpansionTile(
            title: const Text('Make a Payment', style: TextStyle(fontWeight: FontWeight.bold)),
            initiallyExpanded: true,
            children: [
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: [
                    TextField(
                      controller: amountController,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(labelText: 'Amount (₹)', border: OutlineInputBorder(), prefixIcon: Icon(Icons.currency_rupee)),
                    ),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        icon: const Icon(Icons.payment),
                        label: const Text('Pay with PhonePe / UPI'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.purple, 
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                        onPressed: () => _launchUPI(amountController.text),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: txnController,
                      decoration: const InputDecoration(labelText: 'Transaction ID / UPI Ref', border: OutlineInputBorder(), prefixIcon: Icon(Icons.receipt)),
                    ),
                    const SizedBox(height: 16),
                    const Text('Scan to Pay:', style: TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    FutureBuilder<String?>(
                      future: _apiService.getToken(), // Just to get a trigger, actually we construct URL directly
                      builder: (context, snapshot) {
                        // Append timestamp to avoid caching old images
                        final qrUrl = '${ApiService.baseUrl}/static/qrcode.png?v=${DateTime.now().millisecondsSinceEpoch}';
                        return Image.network(
                          qrUrl,
                          height: 200,
                          width: 200,
                          errorBuilder: (context, error, stackTrace) => 
                            Container(
                              height: 150, width: 150, 
                              decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(12)),
                              child: const Center(child: Text('No QR Code Uploaded', textAlign: TextAlign.center)),
                            ),
                        );
                      }
                    ),
                    const SizedBox(height: 16),
                    SizedBox(
                      width: double.infinity,
                      height: 50,
                      child: ElevatedButton(
                        onPressed: () async {
                          if (amountController.text.isEmpty || txnController.text.isEmpty) return;
                          try {
                            await _apiService.createPayment(
                              int.parse(amountController.text),
                              txnController.text,
                            );
                            if (!mounted) return;
                            ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Payment Submitted!')));
                            amountController.clear();
                            txnController.clear();
                            setState(() {}); // Refresh list
                          } catch (e) {
                            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
                          }
                        },
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.green, foregroundColor: Colors.white, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8))),
                        child: const Text('Submit Payment', style: TextStyle(fontSize: 16)),
                      ),
                    )
                  ],
                ),
              ),
            ],
          ),
          
          const Divider(thickness: 4, color: Colors.white),
          
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
               mainAxisAlignment: MainAxisAlignment.spaceBetween,
               children: [
                  const Text('Payment History', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  IconButton(onPressed: () => setState((){}), icon: const Icon(Icons.refresh)),
               ],
            ),
          ),
          
          // Payment Chart (Simple Line Chart for amounts) and List
          FutureBuilder<List<dynamic>>(
            future: _apiService.getMyPayments(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
              if (snapshot.hasError) return Center(child: Text('Error: ${snapshot.error}'));
              
              final payments = snapshot.data ?? [];
              if (payments.isEmpty) return const Center(child: Padding(padding: EdgeInsets.all(20), child: Text('No payment history')));

/*
              // Chart Data Preparation (take last 5 payments)
              final reversedPayments = payments.reversed.take(5).toList();
              final spots = reversedPayments.asMap().entries.map((e) {
                final amt = double.tryParse(e.value['amount'].toString()) ?? 0;
                return FlSpot(e.key.toDouble(), amt);
              }).toList();
*/
              final spots = [];

              return Column(
                children: [
                  if (spots.isNotEmpty)
// Line Chart disabled
                    Container(
                      height: 200,
                      alignment: Alignment.center,
                      child: const Text('Chart Placeholder'),
                    ),

                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: payments.length,
                    itemBuilder: (context, index) {
                      final p = payments[index];
                      return Container(
                         margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                         decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(12)),
                         child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: Colors.green[50], 
                            child: const Icon(Icons.payment, color: Colors.green),
                          ),
                          title: Text('₹${p['amount']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Text(p['created_at'].toString().split('T')[0]),
                          trailing: Chip(
                            label: Text(p['status'], style: TextStyle(fontSize: 12, color: p['status'] == 'Approved' ? Colors.green[900] : Colors.orange[900])),
                            backgroundColor: p['status'] == 'Approved' ? Colors.green[100] : Colors.orange[100],
                            padding: EdgeInsets.zero,
                          ),
                        ),
                      );
                    },
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    
    // We can reuse the widgets from other screens directly or wrap them
    final List<Widget> widgetOptions = [
      _buildHomeTab(),
      _buildPaymentsTab(),
      const FoodMenuScreen(), // Reuse existing screen
      const ComplaintsListScreen(), // Reuse existing screen
    ];

    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: Row(
          children: [
             CircleAvatar(backgroundColor: Colors.white24, child: Text(_userName.isNotEmpty ? _userName[0].toUpperCase() : 'U', style: const TextStyle(color: Colors.white))),
             const SizedBox(width: 12),
             Text(_userName),
          ],
        ),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await _apiService.storage.deleteAll();
              if (mounted) Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: widgetOptions.elementAt(_selectedIndex),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) => setState(() => _selectedIndex = index),
        indicatorColor: Colors.deepOrange.withOpacity(0.2),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.payment_outlined), selectedIcon: Icon(Icons.payment), label: 'Pay'),
          NavigationDestination(icon: Icon(Icons.restaurant_menu_outlined), selectedIcon: Icon(Icons.restaurant_menu), label: 'Food'),
          NavigationDestination(icon: Icon(Icons.report_gmailerrorred_outlined), selectedIcon: Icon(Icons.report), label: 'Issues'),
        ],
      ),
    );
  }
}
