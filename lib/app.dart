import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/tabs.dart';
import 'core/theme.dart';
import 'screens/explore_screen.dart';
import 'screens/home_screen.dart';
import 'screens/map_screen.dart';
import 'screens/settings_screen.dart';
import 'screens/timeline_screen.dart';
import 'state/app_state.dart';

class SteamAtlasApp extends StatelessWidget {
  const SteamAtlasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AppState()..init(),
      // themeMode 가 AppState 에 있으므로 MaterialApp 자체가 상태를 구독해야 한다.
      child: Consumer<AppState>(
        builder: (context, app, _) => MaterialApp(
          title: 'Steam Atlas',
          debugShowCheckedModeBanner: false,
          theme: AppTheme.light(),      // 기본값 — 레이아웃 기준
          darkTheme: AppTheme.dark(),   // 변형
          themeMode: app.themeMode,
          home: const AppShell(),
        ),
      ),
    );
  }
}

class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;

  @override
  Widget build(BuildContext context) {
    final app = context.watch<AppState>();

    if (app.error != null) {
      return Scaffold(
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.error_outline_rounded, size: 40),
                const SizedBox(height: 12),
                const Text('데이터를 불러오지 못했습니다'),
                const SizedBox(height: 6),
                Text('${app.error}', textAlign: TextAlign.center),
              ],
            ),
          ),
        ),
      );
    }

    if (!app.isReady) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final pages = [
      HomeScreen(onJump: (t) => setState(() => _index = t.index)),
      const ExploreScreen(),
      const TimelineScreen(),
      const MapScreen(),
      const SettingsScreen(),
    ];

    return Scaffold(
      body: IndexedStack(index: _index, children: pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home_rounded),
            label: '홈',
          ),
          NavigationDestination(
            icon: Icon(Icons.search_outlined),
            selectedIcon: Icon(Icons.search_rounded),
            label: '탐색',
          ),
          NavigationDestination(
            icon: Icon(Icons.timeline_outlined),
            selectedIcon: Icon(Icons.timeline_rounded),
            label: '연표',
          ),
          NavigationDestination(
            icon: Icon(Icons.map_outlined),
            selectedIcon: Icon(Icons.map_rounded),
            label: '지도',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings_rounded),
            label: '설정',
          ),
        ],
      ),
    );
  }
}
