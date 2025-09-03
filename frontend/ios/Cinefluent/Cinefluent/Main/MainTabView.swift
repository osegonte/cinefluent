import SwiftUI

struct MainTabView: View {
    var body: some View {
        TabView {
            ZStack {
                Color.cinefluent.background.ignoresSafeArea()
                VStack {
                    CinefluentLogo(size: 80)
                    Text("Dashboard")
                        .font(.cinefluent.title)
                        .foregroundColor(.cinefluent.text)
                }
            }
            .tabItem {
                Image(systemName: "house.fill")
                Text("Home")
            }
            
            ZStack {
                Color.cinefluent.background.ignoresSafeArea()
                VStack {
                    CinefluentLogo(size: 80)
                    Text("Movies")
                        .font(.cinefluent.title)
                        .foregroundColor(.cinefluent.text)
                }
            }
            .tabItem {
                Image(systemName: "play.rectangle.fill")
                Text("Movies")
            }
            
            ZStack {
                Color.cinefluent.background.ignoresSafeArea()
                VStack {
                    CinefluentLogo(size: 80)
                    Text("Profile")
                        .font(.cinefluent.title)
                        .foregroundColor(.cinefluent.text)
                }
            }
            .tabItem {
                Image(systemName: "person.fill")
                Text("Profile")
            }
        }
        .accentColor(Color.cinefluent.primary)
    }
}
