def test_transfer_file_rds(
    receiver_rds_page: RdsPage,
    sender_rds_page: RdsPage, 
    rds_protocol_types: List[str],
) -> None:
    sender_rds_page.add_remote_directory(rds_protocol_types, True)
    receiver_rds_page.add_remote_directory(rds_protocol_types, False)
    sender_server_add = FileSystem(True, "sshfs")
    sender_server_add.mount(username="root", password="afra", protocol='sshfs')
    create_files(sender_server_add, path_protocol("sshfs", True), 2, 1000000)
    reciever_server = FileSystem(False, "sshfs")
    reciever_server.mount(username="root", password="afra")
    sender_rds_page.update_action_botton(rds_protocol_types)
    for file in range(2):
        # print(path_protocol("sshfs", True)+"junk"+str(file)+".txt")
        # print(sender_server_add.has_file(path_protocol("sshfs", True), "junk"+str(file)+".txt", "root", "afra"))
        assert sender_server_add.has_file(path_protocol("sshfs", True), "junk"+str(file)+".txt", "root", "afra") != False
        assert reciever_server.has_file(path_protocol("sshfs", False), "junk"+str(file)+".txt", "root", "afra") != False
    sender_server_remove = FileSystem(True, "sshfs")
    sender_server_remove.mount(username="root", password="afra", protocol='sshfs')
    remove_file(sender_server_remove.fs_handler, path_protocol("sshfs", True)+"/junk0.txt")
    sender_rds_page.update_action_botton(rds_protocol_types)
    reciever_server_remove = FileSystem(False, "sshfs")
    reciever_server_remove.mount(username="root", password="afra")
    assert sender_server_remove.has_file(path_protocol("sshfs", True), "junk0.txt", "root", "afra") == False
    assert reciever_server_remove.has_file(path_protocol("sshfs", False), "junk0.txt", "root", "afra") == False
    assert sender_server_remove.has_file(path_protocol(rds_protocol_types, True), "junk0.txt", "root", "afra", True) == reciever_server.has_file(path_protocol(rds_protocol_types, False), "junk0.txt", "root", "afra", True)

