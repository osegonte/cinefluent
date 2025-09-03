import SwiftUI

@main
struct CinefluentApp: App {
    @StateObject private var appCoordinator = AppCoordinator()
    
    var body: some Scene {
        WindowGroup {
            AppCoordinatorView()
                .environmentObject(appCoordinator)
                .preferredColorScheme(.dark)
        }
    }
}
