import 'dart:math' as math;

/// 지도 화면의 카메라 규칙 — 순수 Dart, 위젯 없이 테스트한다.
///
/// 지도는 **상하는 막히고 좌우는 끝없이 도는** 구조다.
/// - 상하: 웹 메르카토르 세계(위도 ±85.05°)의 위아래 끝이 화면 안으로 들어오지 못한다.
///   가장 멀리 축소하면 세계의 세로가 화면 높이에 꼭 맞고, 그때는 상하로 전혀 움직이지 않는다.
/// - 좌우: 경도 180° 를 넘으면 반대편으로 이어진다. 타일·육지 폴리곤·마커가 옆 세계에도 그려진다.
///
/// 이 파일은 그 규칙의 숫자 부분만 담당한다. 실제 제한은 flutter_map 의
/// `CameraConstraint.containLatitude()` 가 하고, 여기서는 그 제한과 맞아떨어지는 최소 줌을 구한다.
class MapGeometry {
  const MapGeometry._();

  /// 웹 메르카토르가 다루는 위도 한계. 이 위도에서 세계가 정확히 정사각형이 된다.
  static const double maxLatitude = 85.0511;

  /// 첫 화면의 중심 경도 — 한국이 가운데 오는 태평양 중심 배치. (프리뷰 HTML 의 MAP_HOME_LON 과 같은 값)
  static const double homeLongitude = 127.5;

  /// 타일 한 변(px). flutter_map 기본값. 줌 z 에서 세계 한 변의 픽셀 = tileDimension × 2^z.
  static const double tileDimension = 256;

  /// 세계의 세로(±85.05°)가 높이 [mapHeightPx] 인 화면을 꼭 채우는 줌.
  ///
  /// 이보다 더 축소하면 세계 위아래 밖의 빈 공간이 보이므로 `containLatitude` 가 이동을 거부한다.
  /// [slack] 만큼 살짝 더 확대해 두어, 부동소수 오차로 '꼭 맞는' 줌이 거부되는 일을 막는다
  /// (0.001 은 세로 약 0.07%, 700px 화면에서 0.5px).
  static double worldFitZoom(
    double mapHeightPx, {
    double tileDimension = tileDimension,
    double slack = 0.001,
  }) {
    if (!mapHeightPx.isFinite || mapHeightPx <= 0) return 1;
    return math.log(mapHeightPx / tileDimension) / math.ln2 + slack;
  }

  /// 줌 [zoom] 에서 세계 한 벌의 한 변(px). 가로로 이 폭만큼 옮기면 같은 그림이 된다(순환 주기).
  static double worldSizePx(double zoom, {double tileDimension = tileDimension}) =>
      tileDimension * math.pow(2, zoom);
}
