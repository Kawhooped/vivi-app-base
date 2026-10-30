package com.ferhatozcelik.jetpackcomposetemplate.navigation

sealed class Screen(val route: String) {
    object Main : Screen("main_screen")
    object Detail : Screen("detail_screen")
    object Story : Screen("story_device")
    object RealityLoom : Screen("reality_loom")
}
