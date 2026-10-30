package com.ferhatozcelik.jetpackcomposetemplate.ui.home

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController

private data class Device(val name: String, val purpose: String, val pipeline: String, val status: String)

private val devices = listOf(
    Device("Story Device", "Turn prompts into coherent worlds, characters and events. Track rules, conflicts and consequences as the story develops.", "Prompt → Interpret → Build → Simulate → Continue", "READY TO USE"),
    Device("City Simulator", "Represent a city as connected systems: residents, housing, work, transit, health, education, environment and public resources.", "Observe → Model → Change → Simulate → Compare", "NEXT"),
    Device("World Builder", "Create reusable environments with entities, properties, relationships, rules, states and events.", "Define → Populate → Connect → Inspect", "PLANNED"),
    Device("Decision Lab", "Compare independent proposals, test assumptions and record predicted outcomes against observed results.", "Question → Propose → Challenge → Decide → Evaluate", "PLANNED")
)

@Composable
fun MainScreen(viewModel: HomeViewModel = hiltViewModel(), navController: NavHostController) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("DEVICE STUDIO", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                Text("Tools that model, build and simulate.", style = MaterialTheme.typography.headlineMedium)
                Text(
                    "A shared architecture for small, useful devices. Each device has a purpose, inputs, internal model, operations and inspectable outputs.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
        items(devices) { device ->
            Card(
                modifier = Modifier.fillMaxWidth().then(
                    if (device.name == "Story Device") Modifier.clickable { navController.navigate("story_device") }
                    else Modifier
                ),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
            ) {
                Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(device.status, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                    Text(device.name, style = MaterialTheme.typography.titleLarge)
                    Text(device.purpose, style = MaterialTheme.typography.bodyMedium)
                    Text(device.pipeline, style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.secondary)
                    if (device.name == "Story Device") Text("OPEN DEVICE  →", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                }
            }
        }
        item {
            Text(
                "CORE RULE: complexity inside, simplicity outside. Models distinguish observed facts, assumptions and unknowns. Decisions and revisions leave a record.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(vertical = 8.dp)
            )
        }
    }
}
