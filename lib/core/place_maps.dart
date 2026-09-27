import 'package:android_intent_plus/android_intent.dart';
import 'package:flutter/foundation.dart'
    show TargetPlatform, defaultTargetPlatform, kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show Clipboard, ClipboardData;
import 'package:url_launcher/url_launcher.dart';

import '../models/locomotive.dart';

/// 보존 위치를 기기의 지도 앱으로 넘긴다.
///
/// 앱 안에서 목록을 따로 그리지 않는다. 안드로이드는 **시스템의 "다음으로 열기" 선택창**
/// (`Intent.createChooser`)을 띄워 기기에 깔린 지도 앱(Google 지도·네이버·TMap·…)을 사용자가 고르게 한다.
/// `createChooser` 는 '항상 이 앱으로' 기본값이 잡혀 있어도 매번 선택창을 띄운다 — 일반 `geo:` 인텐트로
/// 열면 기본 앱으로 곧장 넘어가 버려서 고를 수가 없었다.
///
/// 어느 앱을 고르든 같은 `geo:` 주소가 넘어가므로 주소 하나로 이름이 보이게 만든다:
/// - 시설 공식 명칭(`location.query`)이 있으면 `geo:lat,lng?q=검색어` — 좌표 근처에서 그 이름을 검색해
///   지도 앱이 가진 실제 장소(이름·주소·사진)를 연다. 좌표에 라벨을 붙이는 방식은 Google 지도가
///   라벨을 버리고 좌표만 보여주는 경우가 있어 쓰지 않는다.
/// - 검색어가 없는 곳('각지 보존' 등)은 `geo:0,0?q=lat,lng(라벨)` — 문서화된 라벨 형식으로 좌표 핀.
///
/// iOS 는 시스템 선택창이 없으므로 Apple 지도(`maps://`, 장소명 라벨)로 바로 연다.
/// 그 외·실패 시 브라우저 Google 지도 → 그것도 안 되면 좌표를 복사한다.
class PlaceMaps {
  const PlaceMaps._();

  /// 라벨용 장소명. `geo:` 라벨 파서가 쉼표·괄호를 잘못 다루는 앱이 있어 빼고 넘긴다.
  static String markerTitle(String placeName) => placeName
      .trim()
      .replaceAll(RegExp(r'[(),]'), ' ')
      .replaceAll(RegExp(r'\s+'), ' ')
      .trim();

  /// 안드로이드 인텐트 데이터 (`geo:`). 검색어가 있으면 이름 검색, 없으면 라벨 붙은 좌표 핀.
  static Uri androidUri(LocoLocation loc) {
    final ll = '${loc.lat},${loc.lon}';
    final q = loc.query;
    if (q != null) return Uri.parse('geo:$ll?q=${Uri.encodeComponent(q)}');
    return Uri.parse('geo:0,0?q=$ll(${Uri.encodeComponent(markerTitle(loc.name))})');
  }

  /// Apple 지도. `ll` 과 함께 준 `q` 는 검색어가 아니라 핀의 라벨로 쓰인다.
  static Uri appleUri(LocoLocation loc) => Uri.parse(
      'maps://?ll=${loc.lat},${loc.lon}&q=${Uri.encodeComponent(loc.name)}');

  /// 브라우저 Google 지도. 검색어가 있으면 이름으로, 없으면 좌표로.
  static Uri webUri(LocoLocation loc) => Uri.parse(
      'https://www.google.com/maps/search/?api=1&query='
      '${Uri.encodeComponent(loc.query ?? '${loc.lat},${loc.lon}')}');

  /// '지금 있는 곳' 탭.
  static Future<void> open(BuildContext context, Locomotive loco) async {
    final loc = loco.location;
    if (loc == null) return;
    final messenger = ScaffoldMessenger.of(context);

    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      try {
        // 시스템 선택창 — 기본 앱이 정해져 있어도 매번 뜬다
        await AndroidIntent(
          action: 'action_view',
          data: androidUri(loc).toString(),
        ).launchChooser('지도 앱 선택');
        return;
      } catch (_) {
        // 지도 앱이 하나도 없으면 아래 폴백으로
      }
    } else if (!kIsWeb && defaultTargetPlatform == TargetPlatform.iOS) {
      if (await _launch(appleUri(loc))) return;
    }

    if (await _launch(webUri(loc))) return;
    await _copy(messenger, loc);
  }

  static Future<bool> _launch(Uri uri) async {
    try {
      return await launchUrl(uri, mode: LaunchMode.externalApplication);
    } catch (_) {
      return false;
    }
  }

  static Future<void> _copy(ScaffoldMessengerState messenger, LocoLocation loc) async {
    await Clipboard.setData(
      ClipboardData(text: '${loc.lat}, ${loc.lon} (${loc.name})'),
    );
    messenger.showSnackBar(
      const SnackBar(content: Text('지도 앱을 열지 못해 좌표를 복사했습니다')),
    );
  }

  /// 좌표만 복사 (길게 누르기).
  static Future<void> copyCoordinates(BuildContext context, Locomotive loco) async {
    final loc = loco.location;
    if (loc == null) return;
    final messenger = ScaffoldMessenger.of(context);
    await Clipboard.setData(ClipboardData(text: '${loc.lat}, ${loc.lon}'));
    messenger.showSnackBar(
      SnackBar(content: Text('좌표를 복사했습니다 — ${loc.lat}, ${loc.lon}')),
    );
  }
}
