import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import '../common/notifications_screen.dart';
import '../common/notification_bell.dart';
import 'package:intl/intl.dart';
// import 'package:fl_chart/fl_chart.dart';

class AdminDashboard extends StatefulWidget {
  const AdminDashboard({super.key});

  @override
  State<AdminDashboard> createState() => _AdminDashboardState();
}

class _AdminDashboardState extends State<AdminDashboard> {
  final _apiService = ApiService();
  int _selectedIndex = 0;
  String _userName = 'Admin';

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
  
  // 1. Dashboard Stats
  Widget _buildStatsTab() {
    return FutureBuilder<Map<String, dynamic>>(
      future: _apiService.getStats(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, color: Colors.red, size: 48),
                const SizedBox(height: 16),
                Text('Error loading stats:\n${snapshot.error}', textAlign: TextAlign.center),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () => setState(() {}), 
                  child: const Text('Retry')
                )
              ],
            )
          );
        } else if (!snapshot.hasData) {
          return const Center(child: Text('No stats available'));
        }

        final stats = snapshot.data!;
        // Prepare data for charts
        final activeIssues = double.tryParse(stats['active_issues'].toString()) ?? 0;
        final totalResidents = double.tryParse(stats['total_residents'].toString()) ?? 0;
        // Mocking 'Resolved' for chart demonstration as API might not return it here yet
        final resolvedIssues = (activeIssues * 1.5); 

        return ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
             // --- NEW: Daily Meal Stats ---
             _buildDailyMealStats(),
             const SizedBox(height: 24),

            const Text('Overview', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            
            // Stats Grid
            GridView.count(
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              children: [
                _buildStatCard('Residents', '${stats['total_residents']}', Icons.people, Colors.blue),
                _buildStatCard('Revenue', '₹${stats['revenue']}', Icons.currency_rupee, Colors.green),
                _buildStatCard('Issues', '${stats['active_issues']}', Icons.warning, Colors.orange),
                _buildStatCard('Staff', '${stats['total_staff']}', Icons.badge, Colors.purple),
              ],
            ),
            

            
            const SizedBox(height: 24),
            const Text('Month-wise Revenue', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            
            // Revenue List View inside the stats card
            FutureBuilder<List<dynamic>>(
              future: _apiService.getRevenue(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) return const SizedBox(height: 100, child: Center(child: CircularProgressIndicator()));
                if (snapshot.hasError) return Text('Error: ${snapshot.error}');

                final data = snapshot.data ?? [];
                if (data.isEmpty) return const Center(child: Text('No revenue data recorded yet'));

                return ListView.builder(
                   shrinkWrap: true,
                   physics: const NeverScrollableScrollPhysics(),
                   itemCount: data.length,
                   itemBuilder: (context, index) {
                     final r = data[index];
                     return Card(
                       child: ListTile(
                         leading: const Icon(Icons.calendar_today, color: Colors.green),
                         title: Text(r['month'], style: const TextStyle(fontWeight: FontWeight.bold)),
                         trailing: Text('₹${r['amount']}', style: const TextStyle(fontSize: 18, color: Colors.green, fontWeight: FontWeight.bold)),
                       ),
                     );
                   },
                );
              },
            ),
          ],
        );
      },
    );
  }


  Widget _buildDailyMealStats() {
    final today = DateFormat('yyyy-MM-dd').format(DateTime.now());
    
    return FutureBuilder<Map<String, dynamic>>(
      future: _apiService.getDailyMealStats(today),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const SizedBox();
        final data = snapshot.data!;
        
        return Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.orange[50], // Changed from deepPurple[50]
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.orange.withOpacity(0.2)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                   const Text("Today's Dining Count", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.deepOrange)), // Changed from deepPurple
                   Text(today, style: const TextStyle(fontSize: 12, color: Colors.deepOrange)),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                   _buildMealCountItem("Breakfast", data['breakfast']['eating'], data['breakfast']['opt_out'], Icons.breakfast_dining),
                   _buildMealCountItem("Lunch", data['lunch']['eating'], data['lunch']['opt_out'], Icons.lunch_dining),
                   _buildMealCountItem("Dinner", data['dinner']['eating'], data['dinner']['opt_out'], Icons.dinner_dining),
                ],
              )
            ],
          ),
        );
      },
    );
  }

  Widget _buildMealCountItem(String label, int eating, int optOut, IconData icon) {
    return Column(
      children: [
        CircleAvatar(backgroundColor: Colors.white, radius: 24, child: Icon(icon, color: Colors.deepOrange)), // Changed from deepPurple
        const SizedBox(height: 8),
        Text('$eating', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.deepOrange)), // Changed from green
        Text("Eating", style: TextStyle(fontSize: 10, color: Colors.orange[800])), // Changed from green[800]
        const SizedBox(height: 4),
        if (optOut > 0)
          Text('($optOut Skipping)', style: const TextStyle(fontSize: 11, color: Colors.redAccent, fontWeight: FontWeight.bold))
        else
          const Text('All Eating', style: TextStyle(fontSize: 11, color: Colors.grey)),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
      ],
    );
  }

   Widget _buildStatCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 32),
          const SizedBox(height: 12),
          Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.black87)),
          const SizedBox(height: 4),
          Text(title, style: const TextStyle(color: Colors.grey, fontSize: 12)),
        ],
      ),
    );
  }

  // 2. Residents Management
  Widget _buildResidentsTab() {
    return _ResidentsView(apiService: _apiService);
  }

  // 3. Complaints Management
  Widget _buildComplaintsTab() {
    return FutureBuilder<List<dynamic>>(
      future: _apiService.getAdminComplaints(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(child: Text('Error: ${snapshot.error}'));
        }

        final complaints = snapshot.data ?? [];
        if (complaints.isEmpty) return const Center(child: Text('No complaints found'));

        return ListView.builder(
          itemCount: complaints.length,
          padding: const EdgeInsets.all(8),
          itemBuilder: (context, index) {
            final c = complaints[index];
            final isResolved = c['status'] == 'Resolved';
            return Card(
              elevation: 2,
              margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 4),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              color: isResolved ? Colors.green[50] : Colors.white,
              child: ListTile(
                contentPadding: const EdgeInsets.all(12),
                leading: CircleAvatar(
                  backgroundColor: isResolved ? Colors.green : Colors.orange,
                  child: Icon(isResolved ? Icons.check : Icons.priority_high, color: Colors.white),
                ),
                title: Text(c['category'], style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 6),
                    Text(c['description'], maxLines: 2, overflow: TextOverflow.ellipsis),
                    const SizedBox(height: 6),
                    Row(
                       children: [
                         const Icon(Icons.person, size: 14, color: Colors.grey),
                         const SizedBox(width: 4),
                         Text((c['user'] != null && c['user']['full_name'] != null) ? c['user']['full_name'] : 'Unknown User', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                       ],
                    ),
                  ],
                ),
                trailing: isResolved
                    ? null
                    : ElevatedButton(
                        style: ElevatedButton.styleFrom(
                           backgroundColor: Colors.green,
                           foregroundColor: Colors.white,
                           shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                        ),
                        onPressed: () async {
                          await _apiService.resolveComplaint(c['id']);
                          setState(() {}); // Refresh
                        },
                        child: const Text('Resolve'),
                      ),
              ),
            );
          },
        );
      },
    );
  }

  // 4. Food Menu Update
  Widget _buildFoodMenuTab() {
    final days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    String selectedDay = days.first;
    final breakfastCtrl = TextEditingController();
    final lunchCtrl = TextEditingController();
    final dinnerCtrl = TextEditingController();

    return StatefulBuilder(
      builder: (context, setStateLocal) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
               const Text('Update Weekly Menu', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
               const SizedBox(height: 24),
               
               Container(
                 padding: const EdgeInsets.all(16),
                 decoration: BoxDecoration(
                   color: Colors.white,
                   borderRadius: BorderRadius.circular(12),
                   boxShadow: [BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 10)],
                 ),
                 child: Column(
                   children: [
                      DropdownButtonFormField<String>(
                        value: selectedDay,
                        items: days.map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
                        onChanged: (v) => setStateLocal(() => selectedDay = v!),
                        decoration: const InputDecoration(labelText: 'Select Day', prefixIcon: Icon(Icons.calendar_today)),
                      ),
                      const SizedBox(height: 16),
                      TextField(controller: breakfastCtrl, decoration: const InputDecoration(labelText: 'Breakfast', prefixIcon: Icon(Icons.breakfast_dining), border: OutlineInputBorder())),
                      const SizedBox(height: 12),
                      TextField(controller: lunchCtrl, decoration: const InputDecoration(labelText: 'Lunch', prefixIcon: Icon(Icons.lunch_dining), border: OutlineInputBorder())),
                      const SizedBox(height: 12),
                      TextField(controller: dinnerCtrl, decoration: const InputDecoration(labelText: 'Dinner', prefixIcon: Icon(Icons.dinner_dining), border: OutlineInputBorder())),
                      const SizedBox(height: 24),
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton.icon(
                          icon: const Icon(Icons.save),
                          label: const Text('Save Menu'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.black87,
                            foregroundColor: Colors.white,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                          onPressed: () async {
                            try {
                              await _apiService.updateFoodMenu(selectedDay, breakfastCtrl.text, lunchCtrl.text, dinnerCtrl.text);
                              if (!mounted) return;
                              ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Menu Updated!')));
                              breakfastCtrl.clear(); lunchCtrl.clear(); dinnerCtrl.clear();
                            } catch (e) {
                               ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
                            }
                          },
                        ),

                      ),
                      const SizedBox(height: 12),
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: OutlinedButton.icon(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          label: const Text('Delete Menu for Day', style: TextStyle(color: Colors.red)),
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(color: Colors.red),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                          onPressed: () async {
                             try {
                               await _apiService.deleteFoodMenu(selectedDay);
                               if (!mounted) return;
                               ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Menu for $selectedDay deleted')));
                               breakfastCtrl.clear(); lunchCtrl.clear(); dinnerCtrl.clear();
                             } catch(e) {
                               ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
                             }
                          },
                        ),
                      )
                   ],
                 ),
               ),
            ],
          ),
        );
      },
    );
  }

  // 5. Payment Management
  Widget _buildPaymentsTab() {
    return Column(
      children: [
         Padding(
           padding: const EdgeInsets.all(16.0),
           child: Container(
             padding: const EdgeInsets.all(12),
             decoration: BoxDecoration(
               color: Colors.blue[50],
               borderRadius: BorderRadius.circular(12),
               border: Border.all(color: Colors.blue.withOpacity(0.3)),
             ),
             child: const Row(
               children: [
                 Icon(Icons.info_outline, color: Colors.blue),
                 SizedBox(width: 12),
                 Expanded(
                   child: Text(
                     'Manage incoming payments and approve valid transactions.',
                     style: TextStyle(color: Colors.blue, fontWeight: FontWeight.w500),
                   ),
                 ),
               ],
             ),
           ),
         ),
         Expanded(
           child: FutureBuilder<List<dynamic>>(
            future: _apiService.getAllPayments(),
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
              if (snapshot.hasError) return Center(child: Text('Error: ${snapshot.error}'));

              final payments = snapshot.data ?? [];
              if (payments.isEmpty) return const Center(child: Text('No payments found'));

              return ListView.separated(
                itemCount: payments.length,
                separatorBuilder: (c, i) => const Divider(height: 1),
                itemBuilder: (context, index) {
                  final p = payments[index];
                  final isApproved = p['status'] == 'Approved';
                  
                  return Container(
                    color: p['status'] == 'Pending' ? Colors.orange.withOpacity(0.05) : Colors.transparent,
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: isApproved ? Colors.green[100] : Colors.orange[100],
                        child: Icon(Icons.currency_rupee, color: isApproved ? Colors.green : Colors.orange),
                      ),
                      title: Text('₹${p['amount']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                         Text('${p['user_name']} • ${p['transaction_id']}', maxLines: 1, overflow: TextOverflow.ellipsis),
                         Text(p['created_at'].toString().split('T')[0], style: const TextStyle(fontSize: 12, color: Colors.grey)),
                        ],
                      ),
                      trailing: isApproved
                          ? const Icon(Icons.check_circle, color: Colors.green)
                          : ElevatedButton(
                              style: ElevatedButton.styleFrom(backgroundColor: Colors.green, foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 16)),
                              onPressed: () async {
                                 await _apiService.approvePayment(p['id']);
                                 setState(() {}); // Refresh
                              },
                              child: const Text('Approve'),
                            ),
                    ),
                  );
                },
              );
            },
          ),
         ),
      ],
    );

  }



  @override
  Widget build(BuildContext context) {
    final List<Widget> widgetOptions = [
      _buildStatsTab(),
      _buildResidentsTab(),
      _buildComplaintsTab(),
      _buildFoodMenuTab(),
      _buildPaymentsTab(),
    ];

    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: Row(
          children: [
             CircleAvatar(backgroundColor: Colors.grey[200], child: Text(_userName.isNotEmpty ? _userName[0].toUpperCase() : 'A', style: const TextStyle(color: Colors.black))),
             const SizedBox(width: 12),
             Text(_userName, style: const TextStyle(color: Colors.black)),
          ],
        ),
        actions: [
          const NotificationBell(),
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.red),
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
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard_outlined), selectedIcon: Icon(Icons.dashboard), label: 'Stats'),
          NavigationDestination(icon: Icon(Icons.people_outline), selectedIcon: Icon(Icons.people), label: 'People'),
          NavigationDestination(icon: Icon(Icons.report_gmailerrorred_outlined), selectedIcon: Icon(Icons.report), label: 'Issues'),
          NavigationDestination(icon: Icon(Icons.restaurant_menu_outlined), selectedIcon: Icon(Icons.restaurant_menu), label: 'Food'),
          NavigationDestination(icon: Icon(Icons.payments_outlined), selectedIcon: Icon(Icons.payments), label: 'Pay'),
        ],
      ),
    );
  }
}

// Separate widget for Residents to handle search state properly
class _ResidentsView extends StatefulWidget {
  final ApiService apiService;
  const _ResidentsView({required this.apiService});

  @override
  State<_ResidentsView> createState() => _ResidentsViewState();
}

class _ResidentsViewState extends State<_ResidentsView> {
  final TextEditingController _searchCtrl = TextEditingController();
  List<dynamic> _allResidents = [];
  List<dynamic> _filteredResidents = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadResidents();
  }

  Future<void> _loadResidents() async {
    setState(() => _isLoading = true);
    try {
      final res = await widget.apiService.getResidents();
      if (mounted) {
        setState(() {
          _allResidents = res;
          _filteredResidents = res;
          _isLoading = false;
        });
        _filterResidents(_searchCtrl.text);
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error loading residents: $e')));
      }
    }
  }

  void _filterResidents(String query) {
    if (query.isEmpty) {
      setState(() => _filteredResidents = _allResidents);
    } else {
      setState(() {
        _filteredResidents = _allResidents.where((r) {
          final name = r['full_name'].toString().toLowerCase();
          final email = r['email'].toString().toLowerCase();
          return name.contains(query.toLowerCase()) || email.contains(query.toLowerCase());
        }).toList();
      });
    }
  }

  Future<void> _confirmDeleteUser(int id, String? name) async {
    final displayName = name ?? 'Unknown User';
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Delete $displayName?'),
        content: const Text('This action cannot be undone.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancel')),
          TextButton(onPressed: () => Navigator.pop(context, true), style: TextButton.styleFrom(foregroundColor: Colors.red), child: const Text('Delete')),
        ],
      ),
    );

    if (confirm == true) {
      try {
        await widget.apiService.deleteUser(id);
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Deleted $displayName')));
        _loadResidents();
      } catch (e) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: TextField(
            controller: _searchCtrl,
            onChanged: _filterResidents,
            decoration: InputDecoration(
              hintText: 'Search residents...',
              prefixIcon: const Icon(Icons.search),
              filled: true,
              fillColor: Colors.white,
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
            ),
          ),
        ),
        Expanded(
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : RefreshIndicator(
                  onRefresh: _loadResidents,
                  child: _filteredResidents.isEmpty
                      ? ListView(children: const [Center(child: Padding(padding: EdgeInsets.all(40), child: Text('No residents found')))]) // ListView for refresh capability
                      : ListView.builder(
                          itemCount: _filteredResidents.length,
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          itemBuilder: (context, index) {
                            final resident = _filteredResidents[index];
                            return Card(
                              margin: const EdgeInsets.only(bottom: 12),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                              child: ListTile(
                                contentPadding: const EdgeInsets.all(12),
                                leading: CircleAvatar(
                                  radius: 24,
                                  backgroundColor: Colors.blue[100],
                                  child: Text((resident['full_name'] != null && resident['full_name'].toString().isNotEmpty) ? resident['full_name'][0].toUpperCase() : '?', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blue)),
                                ),
                                title: Text(resident['full_name'] ?? 'Unknown', style: const TextStyle(fontWeight: FontWeight.bold)),
                                subtitle: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(resident['email'] ?? 'No Email'),
                                    const SizedBox(height: 4),
                                    Text('Joined: ${resident['created_at']?.split('T')[0] ?? 'N/A'} • Status: ${resident['status']}', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                                  ],
                                ),
                                trailing: IconButton(
                                  icon: const Icon(Icons.delete_outline, color: Colors.red),
                                  onPressed: () => _confirmDeleteUser(resident['id'], resident['full_name']),
                                ),
                              ),
                            );
                          },
                        ),
                ),
        ),
      ],
    );
  }
}
