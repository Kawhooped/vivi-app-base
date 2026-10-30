package com.ferhatozcelik.jetpackcomposetemplate.ui.story

import android.content.Context
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController

private const val PREFS = "device_studio_story"

@Composable
fun StoryDeviceScreen(navController: NavController) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences(PREFS, Context.MODE_PRIVATE) }
    var premise by remember { mutableStateOf(prefs.getString("premise", "") ?: "") }
    var world by remember { mutableStateOf(prefs.getString("world", "") ?: "") }
    var characters by remember { mutableStateOf(prefs.getString("characters", "") ?: "") }
    var rules by remember { mutableStateOf(prefs.getString("rules", "") ?: "") }
    var state by remember { mutableStateOf(prefs.getString("state", "") ?: "") }
    var output by remember { mutableStateOf(prefs.getString("output", "") ?: "") }
    var turn by remember { mutableStateOf(prefs.getInt("turn", 0)) }
    var status by remember { mutableStateOf("Draft is stored on this device when you tap Save.") }

    fun save() {
        prefs.edit()
            .putString("premise", premise)
            .putString("world", world)
            .putString("characters", characters)
            .putString("rules", rules)
            .putString("state", state)
            .putString("output", output)
            .putInt("turn", turn)
            .apply()
        status = "Saved locally on this device."
    }

    Column(
        modifier = Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        TextButton(onClick = { navController.popBackStack() }) { Text("← Device Studio") }
        Text("STORY DEVICE", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        Text("Build a world. Then let it move.", style = MaterialTheme.typography.headlineMedium)
        Text("A local story model. No account or network connection required.", style = MaterialTheme.typography.bodyMedium)

        OutlinedTextField(
            value = premise, onValueChange = { premise = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("Starting prompt") }, minLines = 3,
            placeholder = { Text("A city where memories can be traded...") }
        )
        OutlinedTextField(
            value = world, onValueChange = { world = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("World and environment") }, minLines = 2
        )
        OutlinedTextField(
            value = characters, onValueChange = { characters = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("Characters and motivations") }, minLines = 2
        )
        OutlinedTextField(
            value = rules, onValueChange = { rules = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("World rules and constraints") }, minLines = 2
        )
        OutlinedTextField(
            value = state, onValueChange = { state = it }, modifier = Modifier.fillMaxWidth(),
            label = { Text("Current situation") }, minLines = 3
        )

        Button(
            onClick = {
                val seed = premise.trim()
                if (seed.isNotEmpty()) {
                    if (world.isBlank()) world = "Environment to define from: $seed"
                    if (characters.isBlank()) characters = "Identify the people affected by this premise, what each wants, and what they fear losing."
                    if (rules.isBlank()) rules = "Define what is possible, what is forbidden, and what every action costs."
                    if (state.isBlank()) state = "Initial condition: $seed"
                    output = "MODEL CREATED\n\nPremise: $seed\n\nWorld: $world\n\nCharacters: $characters\n\nRules: $rules\n\nInitial state: $state\n\nOpen questions:\n• What does each character want?\n• Which rule creates the strongest constraint?\n• What observable event would change the situation?"
                    turn = 0
                    status = "Initial model created. Review and edit every field."
                } else status = "Add a starting prompt first."
            },
            modifier = Modifier.fillMaxWidth()
        ) { Text("Interpret prompt and build model") }

        Button(
            onClick = {
                if (premise.isBlank()) {
                    status = "Create a model before continuing."
                } else {
                    turn += 1
                    val previous = state.ifBlank { premise }
                    val beat = "TURN $turn\n\nStarting condition: $previous\n\nA new pressure enters the system. A character must respond to the rules already defined. Their choice changes the situation, but creates a consequence that remains unresolved.\n\nDecision to make: Which character acts, what do they risk, and what changes as a result?"
                    state = beat
                    output = (output + "\n\n" + beat).trim()
                    status = "Turn $turn added. Edit the outcome to steer the next turn."
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) { Text("Simulate next story turn") }

        Button(onClick = { save() }, modifier = Modifier.fillMaxWidth()) { Text("Save story on this device") }
        TextButton(onClick = {
            premise = ""; world = ""; characters = ""; rules = ""; state = ""; output = ""; turn = 0
            prefs.edit().clear().apply()
            status = "New blank story."
        }) { Text("Start a new story") }

        Text("MODEL OUTPUT", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        Text(if (output.isBlank()) "Your model and story events will appear here." else output, style = MaterialTheme.typography.bodyMedium)
        Text(status, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.secondary)
        Text("Engine note: this first version uses transparent local rules, not a connected generative AI model. Generated turns are scaffolding for your edits.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        Text("Turn count: $turn", style = MaterialTheme.typography.labelMedium)
    }
}
