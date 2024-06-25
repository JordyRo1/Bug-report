#[starknet::interface]
trait Interface<TContractState> {
    fn function_1(self: @TContractState) -> bool; 

    fn function_2(ref self: TContractState, new_bool: bool); 
}

#[starknet::contract]
mod simple_contract{
    use super::Interface;


    #[storage]
    struct Storage {
        index : u32, 
        is_bool: bool
    }

    #[constructor]
    fn constructor(ref self: ContractState, index: u32){
        self.index.write(index);
    }

    #[abi(embed_v0)]
    impl IInterfaceImpl of Interface<ContractState> {
        fn function_1(self: @ContractState) -> bool{
            self.is_bool.read()
        }

        fn function_2(ref self: ContractState, new_bool: bool) {
            self.is_bool.write(new_bool);
        }
    }

}