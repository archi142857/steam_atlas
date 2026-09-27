import 'package:flutter/material.dart';

import 'app.dart';

void main() {
  // shared_preferences 를 runApp 이전에 쓰지는 않지만,
  // 플러그인 채널을 안전하게 초기화하기 위해 명시적으로 바인딩을 띄운다.
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SteamAtlasApp());
}
